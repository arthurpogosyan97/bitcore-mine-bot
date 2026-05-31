from __future__ import annotations

import hashlib
import hmac
import json
import random
import time
import uuid
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import parse_qsl

from aiohttp import web

from config import Config
from db import Database
from game import BOOSTERS, SKINS, UPGRADES, mine_tier, rate_per_hour, storage_capacity, tap_level_for


ROOT = Path(__file__).parent
LAUNCH_GROWTH_PER_SECOND = 1.0


def validate_init_data(init_data: str, bot_token: str) -> dict:
    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = pairs.pop("hash", "")
    if not received_hash:
        raise web.HTTPUnauthorized(reason="Missing Telegram hash")

    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(pairs.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calculated_hash, received_hash):
        raise web.HTTPUnauthorized(reason="Invalid Telegram init data")

    user_raw = pairs.get("user")
    if not user_raw:
        raise web.HTTPUnauthorized(reason="Missing Telegram user")

    return json.loads(user_raw)


def player_name(player) -> str:
    if player["username"]:
        return f"@{player['username']}"
    return player["first_name"] or f"Miner {player['telegram_id']}"


def can_claim_daily(player) -> bool:
    if not player["daily_bonus_at"]:
        return True
    from db import from_iso, utc_now

    return from_iso(player["daily_bonus_at"]).date() != utc_now().date()


def public_state(db: Database, player) -> dict:
    levels = {
        "drill": player["drill_level"],
        "generator": player["generator_level"],
        "storage": player["storage_level"],
    }
    pending = db.pending_mined(player)
    capacity = storage_capacity(player["storage_level"])
    energy, energy_cap = db.energy_state(player)
    tap_level = tap_level_for(player["tap_total"])

    return {
        "player": {
            "id": player["telegram_id"],
            "name": player_name(player),
            "username": player["username"] or "",
            "coins": player["coins"],
            "earnedTotal": db.earned_total(player["telegram_id"]),
            "energy": energy,
            "energyCap": energy_cap,
            "tier": mine_tier(player["generator_level"]),
            "rate": rate_per_hour(player["drill_level"], player["generator_level"]),
            "pending": pending,
            "capacity": capacity,
            "storagePercent": round((pending / capacity) * 100) if capacity else 0,
            "levels": levels,
            "tap": {
                "total": player["tap_total"],
                **tap_level,
            },
            "referralLink": f"https://t.me/BitCoreMineBot?start=ref_{player['telegram_id']}",
            "dailyAvailable": can_claim_daily(player),
            "dailyStreak": player["daily_streak"],
            "referrals": db.referrals_count(player["telegram_id"]),
            "skin": player["skin_key"],
            "team": player["team_name"] or "",
            "boosts": {
                "tap": bool(player["tap_boost_until"]),
                "mine": bool(player["mine_boost_until"]),
            },
        },
        "upgrades": [
            {
                "key": key,
                "title": upgrade.title,
                "icon": upgrade.emoji,
                "description": upgrade.description,
                "level": levels[key],
                "cost": upgrade.cost(levels[key]),
            }
            for key, upgrade in UPGRADES.items()
        ],
        "leaderboard": [
            {"rank": index, "name": player_name(row), "coins": row["coins"]}
            for index, row in enumerate(db.leaderboard(10), start=1)
        ],
        "quests": db.quest_progress(player),
        "achievements": db.achievement_progress(player),
        "boosters": [
            {"key": key, **booster}
            for key, booster in BOOSTERS.items()
        ],
        "skins": [
            {"key": key, **skin, "owned": key in db.owned_skins(player["telegram_id"]), "selected": key == player["skin_key"]}
            for key, skin in SKINS.items()
        ],
    }


def get_authorized_player(request: web.Request):
    config: Config = request.app["config"]
    db: Database = request.app["db"]
    auth = request.headers.get("Authorization", "")
    init_data = auth.removeprefix("tma ").strip() if auth.startswith("tma ") else ""

    if init_data:
        tg_user = validate_init_data(init_data, config.bot_token)
        user = SimpleNamespace(
            id=int(tg_user["id"]),
            username=tg_user.get("username"),
            first_name=tg_user.get("first_name"),
        )
        return db.get_or_create_player(user)

    if config.webapp_dev_user_id:
        user = SimpleNamespace(
            id=config.webapp_dev_user_id,
            username="dev_miner",
            first_name="Dev Miner",
        )
        return db.get_or_create_player(user)

    raise web.HTTPUnauthorized(reason="Open this game from Telegram")


async def index(_: web.Request) -> web.FileResponse:
    return web.FileResponse(ROOT / "miniapp" / "index.html")


async def state(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    return web.json_response(public_state(request.app["db"], player))


async def top_players(request: web.Request) -> web.Response:
    get_authorized_player(request)
    rows = request.app["db"].leaderboard(100)
    return web.json_response(
        {
            "players": [
                {"rank": index, "name": player_name(row), "coins": row["coins"]}
                for index, row in enumerate(rows, start=1)
            ]
        }
    )


async def collect(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    amount, updated = request.app["db"].collect(player["telegram_id"])
    payload = public_state(request.app["db"], updated)
    payload["toast"] = f"Collected {amount} coins" if amount else "Mine is still warming up"
    return web.json_response(payload)


async def daily(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    amount, claimed = request.app["db"].claim_daily_bonus(player["telegram_id"])
    updated = request.app["db"].get_player(player["telegram_id"])
    payload = public_state(request.app["db"], updated)
    payload["toast"] = (
        f"Daily core drop: +{amount} coins"
        if claimed
        else "Daily core drop is already claimed"
    )
    return web.json_response(payload)


async def claim_quest(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    data = await request.json()
    claimed, reward, updated = request.app["db"].claim_quest(player["telegram_id"], data.get("key", ""))
    payload = public_state(request.app["db"], updated)
    payload["toast"] = f"Quest claimed: +{reward}" if claimed else "Quest is not ready yet"
    return web.json_response(payload, status=200 if claimed else 409)


async def claim_achievement(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    data = await request.json()
    claimed, reward, updated = request.app["db"].claim_achievement(player["telegram_id"], data.get("key", ""))
    payload = public_state(request.app["db"], updated)
    payload["toast"] = f"Achievement claimed: +{reward}" if claimed else "Achievement is not ready yet"
    return web.json_response(payload, status=200 if claimed else 409)


async def open_chest(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    updated, reward = request.app["db"].open_chest(player["telegram_id"])
    payload = public_state(request.app["db"], updated)
    payload["chest"] = reward
    payload["toast"] = f"Chest opened: {reward['label']}" if reward["ok"] else reward["label"]
    return web.json_response(payload, status=200 if reward["ok"] else 409)


async def buy_booster(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    data = await request.json()
    bought, updated, cost = request.app["db"].activate_booster(player["telegram_id"], data.get("key", ""))
    payload = public_state(request.app["db"], updated)
    payload["toast"] = f"Booster activated for {cost}" if bought else f"Need {cost} coins for booster"
    return web.json_response(payload, status=200 if bought else 409)


async def buy_skin(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    data = await request.json()
    ok, updated, message, _ = request.app["db"].buy_or_select_skin(player["telegram_id"], data.get("key", "classic"))
    payload = public_state(request.app["db"], updated)
    payload["toast"] = message
    return web.json_response(payload, status=200 if ok else 409)


async def join_team(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    data = await request.json()
    updated = request.app["db"].join_team(player["telegram_id"], data.get("name", "BitCore Pool"))
    payload = public_state(request.app["db"], updated)
    payload["toast"] = f"Joined {updated['team_name']}"
    return web.json_response(payload)


async def upgrade(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    data = await request.json()
    upgrade_key = data.get("key")
    upgrade_info = UPGRADES.get(upgrade_key)
    if not upgrade_info:
        raise web.HTTPBadRequest(reason="Unknown upgrade")

    cost = upgrade_info.cost(player[f"{upgrade_key}_level"])
    if player["coins"] < cost:
        payload = public_state(request.app["db"], player)
        payload["toast"] = "Not enough coins yet"
        return web.json_response(payload, status=409)

    updated = request.app["db"].buy_upgrade(player["telegram_id"], upgrade_key, cost)
    payload = public_state(request.app["db"], updated)
    payload["toast"] = f"{upgrade_info.title} upgraded"
    return web.json_response(payload)


async def tap_coin(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    status, updated, amount = request.app["db"].tap_coin(player["telegram_id"])
    payload = public_state(request.app["db"], updated)
    payload["tap"] = {"status": status, "amount": amount}
    if status == "no_energy":
        payload["toast"] = "Energy is empty. Buy energy or wait."
        return web.json_response(payload, status=409)
    if status == "storage_full":
        payload["toast"] = "Storage is full. Collect coins first."
        return web.json_response(payload, status=409)
    payload["toast"] = f"+{amount} to storage"
    return web.json_response(payload)


async def buy_energy(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    data = await request.json()
    bought, updated, cost = request.app["db"].buy_energy(player["telegram_id"], data.get("pack", "starter"))
    payload = public_state(request.app["db"], updated)
    if not bought:
        payload["toast"] = "Energy is already full" if cost == 0 else f"Need {cost} coins for energy"
        return web.json_response(payload, status=409)
    payload["toast"] = f"Energy pack bought for {cost}"
    return web.json_response(payload)


async def falling_reward(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    data = await request.json()
    caught = max(0, min(int(data.get("caught", 0)), 50))
    reward = caught * 2
    updated = request.app["db"].add_coins(player["telegram_id"], reward, "falling coins") if reward else player
    payload = public_state(request.app["db"], updated)
    payload["drop"] = {"caught": caught, "reward": reward}
    payload["toast"] = f"Drop: caught {caught}, +{reward}" if reward else "Drop: no coins caught"
    return web.json_response(payload)


async def roulette(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    data = await request.json()
    bet = max(10, min(int(data.get("bet", 10)), 500))
    if player["coins"] < bet:
        payload = public_state(request.app["db"], player)
        payload["toast"] = "Not enough coins for this bet"
        return web.json_response(payload, status=409)

    request.app["db"].spend_coins(player["telegram_id"], bet, "roulette bet")
    sectors = [
        {"label": "0", "kind": "miss", "amount": 0, "weight": 24},
        {"label": "+10", "kind": "coin", "amount": 10, "weight": 18},
        {"label": "+20", "kind": "coin", "amount": 20, "weight": 15},
        {"label": "+30", "kind": "coin", "amount": 30, "weight": 12},
        {"label": "0", "kind": "miss", "amount": 0, "weight": 22},
        {"label": "+50", "kind": "coin", "amount": 50, "weight": 8},
        {"label": "x2", "kind": "multiplier", "amount": bet * 2, "weight": 6},
        {"label": "JACKPOT", "kind": "jackpot", "amount": 500, "weight": 1},
    ]
    index = random.choices(range(len(sectors)), weights=[sector["weight"] for sector in sectors], k=1)[0]
    result = sectors[index]
    winnings = int(result["amount"])
    if winnings:
        updated = request.app["db"].add_coins(player["telegram_id"], winnings, "roulette win")
        toast = f"Jackpot +{winnings}" if result["kind"] == "jackpot" else f"You won +{winnings}"
    else:
        updated = request.app["db"].get_player(player["telegram_id"])
        toast = "Missed. Try again"

    payload = public_state(request.app["db"], updated)
    payload["roulette"] = {
        "index": index,
        "label": result["label"],
        "kind": result["kind"],
        "bet": bet,
        "winnings": winnings,
        "sectors": len(sectors),
    }
    payload["toast"] = toast
    return web.json_response(payload)


def launch_crash_multiplier() -> float:
    tier = random.choices(
        ["spark", "steady", "hot", "overdrive", "legend", "mythic"],
        weights=[24, 34, 22, 12, 6, 2],
        k=1,
    )[0]
    ranges = {
        "spark": (1.05, 1.35),
        "steady": (1.36, 2.2),
        "hot": (2.21, 4.0),
        "overdrive": (4.01, 10.0),
        "legend": (10.01, 35.0),
        "mythic": (35.01, 100.0),
    }
    low, high = ranges[tier]
    return min(100, round(random.uniform(low, high), 2))


async def core_launch_start(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    data = await request.json()
    bet = max(10, min(int(data.get("bet", 10)), 500))
    if player["coins"] < bet:
        payload = public_state(request.app["db"], player)
        payload["toast"] = "Not enough coins for launch"
        return web.json_response(payload, status=409)

    request.app["db"].spend_coins(player["telegram_id"], bet, "core launch bet")
    crash_multiplier = launch_crash_multiplier()
    crash_after = max(0.8, (crash_multiplier - 1) / LAUNCH_GROWTH_PER_SECOND)
    round_id = uuid.uuid4().hex
    request.app["launch_rounds"][round_id] = {
        "telegram_id": player["telegram_id"],
        "bet": bet,
        "crash_multiplier": crash_multiplier,
        "crash_after": crash_after,
        "started_at": time.monotonic(),
    }

    updated = request.app["db"].get_player(player["telegram_id"])
    payload = public_state(request.app["db"], updated)
    payload["launch"] = {
        "roundId": round_id,
        "bet": bet,
        "growth": LAUNCH_GROWTH_PER_SECOND,
        "crashAfterMs": int(crash_after * 1000),
    }
    payload["toast"] = "Core launched"
    return web.json_response(payload)


async def core_launch_cashout(request: web.Request) -> web.Response:
    player = get_authorized_player(request)
    data = await request.json()
    round_id = data.get("roundId")
    launch_round = request.app["launch_rounds"].pop(round_id, None)
    if not launch_round or launch_round["telegram_id"] != player["telegram_id"]:
        payload = public_state(request.app["db"], player)
        payload["toast"] = "Launch round expired"
        return web.json_response(payload, status=409)

    elapsed = max(0, time.monotonic() - launch_round["started_at"])
    if elapsed >= launch_round["crash_after"]:
        updated = request.app["db"].get_player(player["telegram_id"])
        payload = public_state(request.app["db"], updated)
        payload["launchResult"] = {
            "status": "crashed",
            "bet": launch_round["bet"],
            "multiplier": launch_round["crash_multiplier"],
            "winnings": 0,
        }
        payload["toast"] = f"Core overheated at x{launch_round['crash_multiplier']:.2f}"
        return web.json_response(payload)

    multiplier = min(
        launch_round["crash_multiplier"],
        1 + elapsed * LAUNCH_GROWTH_PER_SECOND,
    )
    winnings = max(1, int(launch_round["bet"] * multiplier))
    updated = request.app["db"].add_coins(player["telegram_id"], winnings, "core launch win")
    payload = public_state(request.app["db"], updated)
    payload["launchResult"] = {
        "status": "cashed",
        "bet": launch_round["bet"],
        "multiplier": round(multiplier, 2),
        "winnings": winnings,
    }
    payload["toast"] = f"Core secured x{multiplier:.2f}: +{winnings}"
    return web.json_response(payload)


def create_web_app(config: Config, db: Database) -> web.Application:
    app = web.Application()
    app["config"] = config
    app["db"] = db
    app["launch_rounds"] = {}
    app.router.add_get("/", index)
    app.router.add_get("/api/state", state)
    app.router.add_get("/api/leaderboard", top_players)
    app.router.add_post("/api/collect", collect)
    app.router.add_post("/api/daily", daily)
    app.router.add_post("/api/quest/claim", claim_quest)
    app.router.add_post("/api/achievement/claim", claim_achievement)
    app.router.add_post("/api/chest/open", open_chest)
    app.router.add_post("/api/booster/buy", buy_booster)
    app.router.add_post("/api/skin/buy", buy_skin)
    app.router.add_post("/api/team/join", join_team)
    app.router.add_post("/api/upgrade", upgrade)
    app.router.add_post("/api/tap", tap_coin)
    app.router.add_post("/api/energy/buy", buy_energy)
    app.router.add_post("/api/falling/reward", falling_reward)
    app.router.add_post("/api/roulette", roulette)
    app.router.add_post("/api/core-launch/start", core_launch_start)
    app.router.add_post("/api/core-launch/cashout", core_launch_cashout)
    app.router.add_static("/static", ROOT / "miniapp", show_index=False)
    app.router.add_static("/assets", ROOT, show_index=False)
    return app


async def start_web_app(config: Config, db: Database) -> web.AppRunner:
    runner = web.AppRunner(create_web_app(config, db))
    await runner.setup()
    site = web.TCPSite(runner, config.webapp_host, config.webapp_port)
    await site.start()
    return runner
