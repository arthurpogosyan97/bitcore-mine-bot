from __future__ import annotations

import sqlite3
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from game import (
    START_COINS,
    START_ENERGY,
    ENERGY_REGEN_SECONDS,
    ACHIEVEMENTS,
    BOOSTERS,
    CHEST_REWARDS,
    DAILY_QUESTS,
    SKINS,
    max_energy,
    rate_per_hour,
    storage_capacity,
    tap_level_for,
)


def utc_now() -> datetime:
    return datetime.now(UTC)


def to_iso(value: datetime) -> str:
    return value.isoformat()


def from_iso(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


class Database:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row

    def init(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS players (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                coins INTEGER NOT NULL,
                energy INTEGER NOT NULL,
                drill_level INTEGER NOT NULL,
                generator_level INTEGER NOT NULL,
                storage_level INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                last_collected_at TEXT NOT NULL,
                daily_bonus_at TEXT,
                banned INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        self._migrate_players()
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS quest_claims (
                telegram_id INTEGER NOT NULL,
                quest_key TEXT NOT NULL,
                claimed_date TEXT NOT NULL,
                PRIMARY KEY (telegram_id, quest_key, claimed_date)
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS achievement_claims (
                telegram_id INTEGER NOT NULL,
                achievement_key TEXT NOT NULL,
                claimed_at TEXT NOT NULL,
                PRIMARY KEY (telegram_id, achievement_key)
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS player_skins (
                telegram_id INTEGER NOT NULL,
                skin_key TEXT NOT NULL,
                bought_at TEXT NOT NULL,
                PRIMARY KEY (telegram_id, skin_key)
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self.conn.execute(
            """
            INSERT OR IGNORE INTO player_skins (telegram_id, skin_key, bought_at)
            SELECT telegram_id, 'classic', created_at FROM players
            """
        )
        self.conn.commit()

    def _migrate_players(self) -> None:
        columns = {
            row["name"]
            for row in self.conn.execute("PRAGMA table_info(players)").fetchall()
        }
        migrations = {
            "stored_coins": "ALTER TABLE players ADD COLUMN stored_coins INTEGER NOT NULL DEFAULT 0",
            "tap_total": "ALTER TABLE players ADD COLUMN tap_total INTEGER NOT NULL DEFAULT 0",
            "energy_updated_at": "ALTER TABLE players ADD COLUMN energy_updated_at TEXT",
            "referrer_id": "ALTER TABLE players ADD COLUMN referrer_id INTEGER",
            "daily_streak": "ALTER TABLE players ADD COLUMN daily_streak INTEGER NOT NULL DEFAULT 0",
            "tap_boost_until": "ALTER TABLE players ADD COLUMN tap_boost_until TEXT",
            "mine_boost_until": "ALTER TABLE players ADD COLUMN mine_boost_until TEXT",
            "skin_key": "ALTER TABLE players ADD COLUMN skin_key TEXT NOT NULL DEFAULT 'classic'",
            "team_name": "ALTER TABLE players ADD COLUMN team_name TEXT",
        }
        for column, sql in migrations.items():
            if column not in columns:
                self.conn.execute(sql)
        self.conn.commit()

    def _boost_active(self, player: sqlite3.Row, column: str) -> bool:
        value = player[column]
        return bool(value and from_iso(value) > utc_now())

    def get_or_create_player(self, user: Any) -> sqlite3.Row:
        player = self.get_player(user.id)
        if player:
            self.conn.execute(
                "UPDATE players SET username = ?, first_name = ? WHERE telegram_id = ?",
                (user.username, user.first_name, user.id),
            )
            self.conn.commit()
            return self.get_player(user.id)

        now = to_iso(utc_now())
        self.conn.execute(
            """
            INSERT INTO players (
                telegram_id, username, first_name, coins, energy,
                drill_level, generator_level, storage_level,
                created_at, last_collected_at
            )
            VALUES (?, ?, ?, ?, ?, 1, 1, 1, ?, ?)
            """,
            (user.id, user.username, user.first_name, START_COINS, START_ENERGY, now, now),
        )
        self.conn.execute(
            "UPDATE players SET energy_updated_at = ? WHERE telegram_id = ?",
            (now, user.id),
        )
        self.add_transaction(user.id, START_COINS, "registration bonus", commit=False)
        self.conn.commit()
        return self.get_player(user.id)

    def get_player(self, telegram_id: int) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM players WHERE telegram_id = ?",
            (telegram_id,),
        ).fetchone()

    def set_referrer(self, telegram_id: int, referrer_id: int) -> bool:
        player = self.get_player(telegram_id)
        referrer = self.get_player(referrer_id)
        if not player or not referrer or telegram_id == referrer_id or player["referrer_id"]:
            return False
        self.conn.execute(
            "UPDATE players SET referrer_id = ? WHERE telegram_id = ?",
            (referrer_id, telegram_id),
        )
        self.conn.execute(
            "UPDATE players SET coins = coins + ? WHERE telegram_id = ?",
            (100, referrer_id),
        )
        self.add_transaction(referrer_id, 100, "referral bonus", commit=False)
        self.conn.commit()
        return True

    def count_players(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) AS count FROM players").fetchone()
        return int(row["count"])

    def total_coins(self) -> int:
        row = self.conn.execute("SELECT COALESCE(SUM(coins), 0) AS total FROM players").fetchone()
        return int(row["total"])

    def earned_total(self, telegram_id: int) -> int:
        row = self.conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM transactions
            WHERE telegram_id = ? AND amount > 0
            """,
            (telegram_id,),
        ).fetchone()
        return int(row["total"])

    def leaderboard(self, limit: int = 10) -> list[sqlite3.Row]:
        return self.conn.execute(
            """
            SELECT * FROM players
            WHERE banned = 0
            ORDER BY coins DESC, drill_level + generator_level + storage_level DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    def _passive_mined(self, player: sqlite3.Row) -> int:
        elapsed = max((utc_now() - from_iso(player["last_collected_at"])).total_seconds(), 0)
        hourly_rate = rate_per_hour(player["drill_level"], player["generator_level"])
        if self._boost_active(player, "mine_boost_until"):
            hourly_rate *= 2
        return int(hourly_rate * elapsed / 3600)

    def pending_mined(self, player: sqlite3.Row) -> int:
        stored = player["stored_coins"] + self._passive_mined(player)
        return min(stored, storage_capacity(player["storage_level"]))

    def energy_state(self, player: sqlite3.Row) -> tuple[int, int]:
        cap = max_energy(player["generator_level"])
        updated_raw = player["energy_updated_at"] or player["last_collected_at"]
        elapsed = max((utc_now() - from_iso(updated_raw)).total_seconds(), 0)
        regenerated = int(elapsed // ENERGY_REGEN_SECONDS)
        energy = min(cap, player["energy"] + regenerated)
        if regenerated > 0 and energy != player["energy"]:
            self.conn.execute(
                "UPDATE players SET energy = ?, energy_updated_at = ? WHERE telegram_id = ?",
                (energy, to_iso(utc_now()), player["telegram_id"]),
            )
            self.conn.commit()
        return energy, cap

    def collect(self, telegram_id: int) -> tuple[int, sqlite3.Row]:
        player = self.get_player(telegram_id)
        if not player:
            raise ValueError("Player not found")

        amount = self.pending_mined(player)
        now = to_iso(utc_now())
        if amount > 0:
            self.conn.execute(
                """
                UPDATE players
                SET coins = coins + ?, stored_coins = 0, last_collected_at = ?
                WHERE telegram_id = ?
                """,
                (amount, now, telegram_id),
            )
            self.add_transaction(telegram_id, amount, "mine collect", commit=False)
        else:
            self.conn.execute(
                "UPDATE players SET stored_coins = 0, last_collected_at = ? WHERE telegram_id = ?",
                (now, telegram_id),
            )
        self.conn.commit()
        return amount, self.get_player(telegram_id)

    def tap_coin(self, telegram_id: int) -> tuple[str, sqlite3.Row, int]:
        player = self.get_player(telegram_id)
        if not player:
            raise ValueError("Player not found")

        energy, _ = self.energy_state(player)
        player = self.get_player(telegram_id)
        if energy <= 0:
            return "no_energy", player, 0

        pending = self.pending_mined(player)
        capacity = storage_capacity(player["storage_level"])
        if pending >= capacity:
            return "storage_full", player, 0

        tap_info = tap_level_for(player["tap_total"])
        tap_power = tap_info["tapPower"] * (2 if self._boost_active(player, "tap_boost_until") else 1)
        amount = min(tap_power, capacity - pending)
        passive = self._passive_mined(player)
        new_stored = min(capacity, player["stored_coins"] + passive + amount)
        now = to_iso(utc_now())

        self.conn.execute(
            """
            UPDATE players
            SET stored_coins = ?, last_collected_at = ?, energy = ?, energy_updated_at = ?,
                tap_total = tap_total + ?
            WHERE telegram_id = ?
            """,
            (new_stored, now, energy - 1, now, amount, telegram_id),
        )
        self.add_transaction(telegram_id, amount, "tap stored", commit=False)
        self.conn.commit()
        return "ok", self.get_player(telegram_id), amount

    def buy_energy(self, telegram_id: int, pack_key: str = "starter") -> tuple[bool, sqlite3.Row, int]:
        player = self.get_player(telegram_id)
        if not player:
            raise ValueError("Player not found")
        packs = {
            "starter": {"energy": 25, "cost": 50},
            "worker": {"energy": 60, "cost": 110},
            "reactor": {"energy": 140, "cost": 240},
            "quantum": {"energy": 320, "cost": 500},
            "unlimited": {"energy": 9999, "cost": 1200},
        }
        pack = packs.get(pack_key, packs["starter"])
        cost = pack["cost"]
        energy, cap = self.energy_state(player)
        player = self.get_player(telegram_id)
        if energy >= cap:
            return False, player, 0
        if player["coins"] < cost:
            return False, player, cost

        new_energy = min(cap, energy + pack["energy"])
        now = to_iso(utc_now())
        self.conn.execute(
            "UPDATE players SET coins = coins - ?, energy = ?, energy_updated_at = ? WHERE telegram_id = ?",
            (cost, new_energy, now, telegram_id),
        )
        self.add_transaction(telegram_id, -cost, "energy pack", commit=False)
        self.conn.commit()
        return True, self.get_player(telegram_id), cost

    def buy_upgrade(self, telegram_id: int, upgrade_key: str, cost: int) -> sqlite3.Row:
        column = f"{upgrade_key}_level"
        if column not in {"drill_level", "generator_level", "storage_level"}:
            raise ValueError("Unknown upgrade")

        player = self.get_player(telegram_id)
        if not player:
            raise ValueError("Player not found")
        if player["coins"] < cost:
            raise ValueError("Not enough coins")

        self.conn.execute(
            f"UPDATE players SET coins = coins - ?, {column} = {column} + 1 WHERE telegram_id = ?",
            (cost, telegram_id),
        )
        self.add_transaction(telegram_id, -cost, f"upgrade {upgrade_key}", commit=False)
        self.conn.commit()
        return self.get_player(telegram_id)

    def claim_daily_bonus(self, telegram_id: int) -> tuple[int, bool]:
        player = self.get_player(telegram_id)
        if not player:
            raise ValueError("Player not found")

        now = utc_now()
        if player["daily_bonus_at"]:
            last = from_iso(player["daily_bonus_at"])
            if last.date() == now.date():
                return 0, False

        last = from_iso(player["daily_bonus_at"]) if player["daily_bonus_at"] else None
        streak = player["daily_streak"] + 1 if last and (now.date() - last.date()).days == 1 else 1
        amount = 75 + player["generator_level"] * 10 + min(streak, 7) * 15
        self.conn.execute(
            "UPDATE players SET coins = coins + ?, daily_bonus_at = ?, daily_streak = ? WHERE telegram_id = ?",
            (amount, to_iso(now), streak, telegram_id),
        )
        self.add_transaction(telegram_id, amount, "daily bonus", commit=False)
        self.conn.commit()
        return amount, True

    def transaction_count(self, telegram_id: int, reason: str) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) AS count FROM transactions WHERE telegram_id = ? AND reason = ?",
            (telegram_id, reason),
        ).fetchone()
        return int(row["count"])

    def referrals_count(self, telegram_id: int) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) AS count FROM players WHERE referrer_id = ?",
            (telegram_id,),
        ).fetchone()
        return int(row["count"])

    def player_stats(self, player: sqlite3.Row) -> dict:
        telegram_id = player["telegram_id"]
        return {
            "tap_total": player["tap_total"],
            "coins": player["coins"],
            "collects": self.transaction_count(telegram_id, "mine collect"),
            "launches": self.transaction_count(telegram_id, "core launch bet"),
            "wheels": self.transaction_count(telegram_id, "roulette bet"),
            "referrals": self.referrals_count(telegram_id),
        }

    def quest_progress(self, player: sqlite3.Row) -> list[dict]:
        stats = self.player_stats(player)
        today = utc_now().date().isoformat()
        claimed = {
            row["quest_key"]
            for row in self.conn.execute(
                "SELECT quest_key FROM quest_claims WHERE telegram_id = ? AND claimed_date = ?",
                (player["telegram_id"], today),
            ).fetchall()
        }
        progress_map = {
            "tap_25": (min(stats["tap_total"], 25), 25),
            "collect_1": (min(stats["collects"], 1), 1),
            "launch_1": (min(stats["launches"], 1), 1),
            "wheel_1": (min(stats["wheels"], 1), 1),
        }
        quests = []
        for quest in DAILY_QUESTS:
            current, target = progress_map[quest["key"]]
            quests.append({**quest, "current": current, "target": target, "done": current >= target, "claimed": quest["key"] in claimed})
        return quests

    def claim_quest(self, telegram_id: int, quest_key: str) -> tuple[bool, int, sqlite3.Row]:
        player = self.get_player(telegram_id)
        quests = {quest["key"]: quest for quest in self.quest_progress(player)}
        quest = quests.get(quest_key)
        if not quest or not quest["done"] or quest["claimed"]:
            return False, 0, player
        today = utc_now().date().isoformat()
        self.conn.execute(
            "INSERT INTO quest_claims (telegram_id, quest_key, claimed_date) VALUES (?, ?, ?)",
            (telegram_id, quest_key, today),
        )
        self.conn.execute("UPDATE players SET coins = coins + ? WHERE telegram_id = ?", (quest["reward"], telegram_id))
        self.add_transaction(telegram_id, quest["reward"], f"quest {quest_key}", commit=False)
        self.conn.commit()
        return True, quest["reward"], self.get_player(telegram_id)

    def achievement_progress(self, player: sqlite3.Row) -> list[dict]:
        stats = self.player_stats(player)
        claimed = {
            row["achievement_key"]
            for row in self.conn.execute(
                "SELECT achievement_key FROM achievement_claims WHERE telegram_id = ?",
                (player["telegram_id"],),
            ).fetchall()
        }
        done_map = {
            "first_tap": stats["tap_total"] >= 1,
            "tap_100": stats["tap_total"] >= 100,
            "collector": stats["collects"] >= 5,
            "launcher": stats["launches"] >= 5,
            "rich_1000": stats["coins"] >= 1000,
            "ref_1": stats["referrals"] >= 1,
            "ref_5": stats["referrals"] >= 5,
        }
        return [{**item, "done": done_map[item["key"]], "claimed": item["key"] in claimed} for item in ACHIEVEMENTS]

    def claim_achievement(self, telegram_id: int, achievement_key: str) -> tuple[bool, int, sqlite3.Row]:
        player = self.get_player(telegram_id)
        achievements = {item["key"]: item for item in self.achievement_progress(player)}
        achievement = achievements.get(achievement_key)
        if not achievement or not achievement["done"] or achievement["claimed"]:
            return False, 0, player
        self.conn.execute(
            "INSERT INTO achievement_claims (telegram_id, achievement_key, claimed_at) VALUES (?, ?, ?)",
            (telegram_id, achievement_key, to_iso(utc_now())),
        )
        self.conn.execute("UPDATE players SET coins = coins + ? WHERE telegram_id = ?", (achievement["reward"], telegram_id))
        self.add_transaction(telegram_id, achievement["reward"], f"achievement {achievement_key}", commit=False)
        self.conn.commit()
        return True, achievement["reward"], self.get_player(telegram_id)

    def add_energy(self, telegram_id: int, amount: int, reason: str) -> sqlite3.Row:
        player = self.get_player(telegram_id)
        energy, cap = self.energy_state(player)
        now = to_iso(utc_now())
        self.conn.execute(
            "UPDATE players SET energy = ?, energy_updated_at = ? WHERE telegram_id = ?",
            (min(cap, energy + amount), now, telegram_id),
        )
        self.add_transaction(telegram_id, 0, reason, commit=False)
        self.conn.commit()
        return self.get_player(telegram_id)

    def activate_booster(self, telegram_id: int, booster_key: str, *, paid: bool = True) -> tuple[bool, sqlite3.Row, int]:
        player = self.get_player(telegram_id)
        booster = BOOSTERS.get(booster_key)
        if not booster:
            return False, player, 0
        if paid and player["coins"] < booster["cost"]:
            return False, player, booster["cost"]
        column = "tap_boost_until" if booster_key == "tap_x2" else "mine_boost_until"
        until = to_iso(utc_now() + timedelta(minutes=booster["minutes"]))
        if paid:
            self.conn.execute("UPDATE players SET coins = coins - ?, " + column + " = ? WHERE telegram_id = ?", (booster["cost"], until, telegram_id))
            self.add_transaction(telegram_id, -booster["cost"], f"booster {booster_key}", commit=False)
        else:
            self.conn.execute("UPDATE players SET " + column + " = ? WHERE telegram_id = ?", (until, telegram_id))
        self.conn.commit()
        return True, self.get_player(telegram_id), booster["cost"]

    def open_chest(self, telegram_id: int) -> tuple[sqlite3.Row, dict]:
        player = self.get_player(telegram_id)
        cost = 75
        if player["coins"] < cost:
            return player, {"ok": False, "label": "Need 75 coins", "cost": cost}
        reward = random.choices(CHEST_REWARDS, weights=[item["weight"] for item in CHEST_REWARDS], k=1)[0]
        self.spend_coins(telegram_id, cost, "chest open")
        if reward["kind"] == "energy":
            updated = self.add_energy(telegram_id, reward["amount"], "chest energy")
        elif reward["kind"] == "booster":
            _, updated, _ = self.activate_booster(telegram_id, "tap_x2", paid=False)
        else:
            updated = self.add_coins(telegram_id, reward["amount"], "chest reward")
        return updated, {"ok": True, **reward, "cost": cost}

    def owned_skins(self, telegram_id: int) -> set[str]:
        return {
            row["skin_key"]
            for row in self.conn.execute(
                "SELECT skin_key FROM player_skins WHERE telegram_id = ?",
                (telegram_id,),
            ).fetchall()
        }

    def buy_or_select_skin(self, telegram_id: int, skin_key: str) -> tuple[bool, sqlite3.Row, str, int]:
        player = self.get_player(telegram_id)
        skin = SKINS.get(skin_key)
        if not skin:
            return False, player, "Unknown skin", 0
        owned = self.owned_skins(telegram_id)
        if skin_key not in owned:
            if player["coins"] < skin["cost"]:
                return False, player, "Not enough coins for skin", skin["cost"]
            self.conn.execute("UPDATE players SET coins = coins - ? WHERE telegram_id = ?", (skin["cost"], telegram_id))
            self.conn.execute(
                "INSERT INTO player_skins (telegram_id, skin_key, bought_at) VALUES (?, ?, ?)",
                (telegram_id, skin_key, to_iso(utc_now())),
            )
            self.add_transaction(telegram_id, -skin["cost"], f"skin {skin_key}", commit=False)
        self.conn.execute("UPDATE players SET skin_key = ? WHERE telegram_id = ?", (skin_key, telegram_id))
        self.conn.commit()
        return True, self.get_player(telegram_id), "Skin selected", skin["cost"]

    def join_team(self, telegram_id: int, team_name: str) -> sqlite3.Row:
        team = team_name.strip()[:24] or "BitCore Pool"
        self.conn.execute("UPDATE players SET team_name = ? WHERE telegram_id = ?", (team, telegram_id))
        self.conn.commit()
        return self.get_player(telegram_id)

    def grant(self, telegram_id: int, amount: int) -> bool:
        if not self.get_player(telegram_id):
            return False
        self.conn.execute(
            "UPDATE players SET coins = coins + ? WHERE telegram_id = ?",
            (amount, telegram_id),
        )
        self.add_transaction(telegram_id, amount, "admin grant", commit=False)
        self.conn.commit()
        return True

    def add_coins(self, telegram_id: int, amount: int, reason: str) -> sqlite3.Row:
        player = self.get_player(telegram_id)
        if not player:
            raise ValueError("Player not found")

        self.conn.execute(
            "UPDATE players SET coins = coins + ? WHERE telegram_id = ?",
            (amount, telegram_id),
        )
        self.add_transaction(telegram_id, amount, reason, commit=False)
        self.conn.commit()
        return self.get_player(telegram_id)

    def spend_coins(self, telegram_id: int, amount: int, reason: str) -> sqlite3.Row:
        player = self.get_player(telegram_id)
        if not player:
            raise ValueError("Player not found")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if player["coins"] < amount:
            raise ValueError("Not enough coins")

        self.conn.execute(
            "UPDATE players SET coins = coins - ? WHERE telegram_id = ?",
            (amount, telegram_id),
        )
        self.add_transaction(telegram_id, -amount, reason, commit=False)
        self.conn.commit()
        return self.get_player(telegram_id)

    def add_transaction(
        self,
        telegram_id: int,
        amount: int,
        reason: str,
        *,
        commit: bool = True,
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO transactions (telegram_id, amount, reason, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (telegram_id, amount, reason, to_iso(utc_now())),
        )
        if commit:
            self.conn.commit()
