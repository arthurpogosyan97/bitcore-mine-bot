from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, MenuButtonWebApp, Message, WebAppInfo
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import load_config
from db import Database
from game import UPGRADES, mine_tier, rate_per_hour, storage_capacity
from keyboards import launch_app_button, main_menu, upgrades_menu
from webapp import create_web_app, start_web_app


logging.basicConfig(level=logging.INFO)

config = load_config()
db = Database(config.db_path)
dp = Dispatcher()


def is_admin(telegram_id: int) -> bool:
    return telegram_id in config.admin_ids


def menu_markup():
    return main_menu(config.mini_app_url)


def player_title(player) -> str:
    if player["username"]:
        return f"@{player['username']}"
    return player["first_name"] or str(player["telegram_id"])


def profile_text(player) -> str:
    rate = rate_per_hour(player["drill_level"], player["generator_level"])
    capacity = storage_capacity(player["storage_level"])
    pending = db.pending_mined(player)
    tier = mine_tier(player["generator_level"])

    return (
        "BitCore Mine Profile\n\n"
        f"Player: {player_title(player)}\n"
        f"Tier: {tier}\n"
        f"Coins: {player['coins']}\n"
        f"Energy: {player['energy']}\n\n"
        f"Plasma Drill: Lv.{player['drill_level']}\n"
        f"Bit Reactor: Lv.{player['generator_level']}\n"
        f"Core Vault: Lv.{player['storage_level']}\n\n"
        f"Mining rate: {rate} coins/hour\n"
        f"Storage: {pending}/{capacity} coins"
    )


@dp.message(Command("start"))
async def start(message: Message) -> None:
    player = db.get_or_create_player(message.from_user)
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) > 1 and parts[1].startswith("ref_"):
        try:
            db.set_referrer(message.from_user.id, int(parts[1].removeprefix("ref_")))
            player = db.get_player(message.from_user.id)
        except ValueError:
            pass
    await message.answer(
        "Welcome to BitCore Mine.\n\n"
        "Your starter shaft is online. Mine digital cores, collect coins, "
        "upgrade your rig, and climb the leaderboard.",
        reply_markup=menu_markup(),
    )
    if config.mini_app_url:
        await message.answer(
            "Open the Mini App to play BitCore Mine as a real game screen.",
            reply_markup=launch_app_button(config.mini_app_url),
        )
    else:
        await message.answer(
            "Mini App UI is ready. Add a public HTTPS URL to MINI_APP_URL "
            "to show the game button inside Telegram."
        )
    await message.answer(profile_text(player))


@dp.message(Command("menu"))
async def menu(message: Message) -> None:
    db.get_or_create_player(message.from_user)
    await message.answer("Main menu:", reply_markup=menu_markup())


@dp.message(Command("profile"))
@dp.message(F.text == "Profile")
async def profile(message: Message) -> None:
    player = db.get_or_create_player(message.from_user)
    await message.answer(profile_text(player), reply_markup=menu_markup())


@dp.message(Command("mine"))
@dp.message(F.text == "Mine")
async def mine(message: Message) -> None:
    player = db.get_or_create_player(message.from_user)
    pending = db.pending_mined(player)
    capacity = storage_capacity(player["storage_level"])
    rate = rate_per_hour(player["drill_level"], player["generator_level"])
    await message.answer(
        "Mine Status\n\n"
        f"Zone: {mine_tier(player['generator_level'])}\n"
        f"Stored: {pending}/{capacity} coins\n"
        f"Rate: {rate} coins/hour\n\n"
        "Press Collect to move mined coins into your wallet.",
        reply_markup=menu_markup(),
    )


@dp.message(Command("collect"))
@dp.message(F.text == "Collect")
async def collect(message: Message) -> None:
    db.get_or_create_player(message.from_user)
    amount, player = db.collect(message.from_user.id)
    if amount <= 0:
        await message.answer(
            "The rigs are still warming up. Come back soon to collect more coins.",
            reply_markup=menu_markup(),
        )
        return

    await message.answer(
        f"Collected {amount} coins.\n\n"
        f"Wallet balance: {player['coins']} coins",
        reply_markup=menu_markup(),
    )


@dp.message(Command("upgrades"))
@dp.message(F.text == "Upgrades")
async def upgrades(message: Message) -> None:
    player = db.get_or_create_player(message.from_user)
    levels = {
        "drill": player["drill_level"],
        "generator": player["generator_level"],
        "storage": player["storage_level"],
    }
    await message.answer(
        "Upgrade Market\n\n"
        "Improve your rig to mine faster and store more coins.",
        reply_markup=upgrades_menu(levels),
    )


@dp.callback_query(F.data.startswith("upgrade:"))
async def buy_upgrade(callback: CallbackQuery) -> None:
    player = db.get_or_create_player(callback.from_user)
    upgrade_key = callback.data.split(":", 1)[1]
    upgrade = UPGRADES.get(upgrade_key)
    if not upgrade:
        await callback.answer("Unknown upgrade.", show_alert=True)
        return

    current_level = player[f"{upgrade_key}_level"]
    cost = upgrade.cost(current_level)
    if player["coins"] < cost:
        await callback.answer("Not enough coins yet.", show_alert=True)
        return

    updated = db.buy_upgrade(callback.from_user.id, upgrade_key, cost)
    await callback.answer(f"{upgrade.title} upgraded.")
    await callback.message.answer(
        f"{upgrade.title} is now Lv.{updated[f'{upgrade_key}_level']}.\n"
        f"Coins left: {updated['coins']}",
        reply_markup=menu_markup(),
    )


@dp.message(Command("tasks"))
@dp.message(F.text == "Tasks")
async def tasks(message: Message) -> None:
    db.get_or_create_player(message.from_user)
    amount, claimed = db.claim_daily_bonus(message.from_user.id)
    if claimed:
        await message.answer(
            f"Daily bonus claimed: {amount} coins.\n\n"
            "Daily task: collect from your mine and buy one upgrade.",
            reply_markup=menu_markup(),
        )
    else:
        await message.answer(
            "You already claimed today's bonus.\n\n"
            "Come back tomorrow for another core drop.",
            reply_markup=menu_markup(),
        )


@dp.message(Command("leaderboard"))
@dp.message(F.text == "Leaderboard")
async def leaderboard(message: Message) -> None:
    db.get_or_create_player(message.from_user)
    rows = db.leaderboard()
    if not rows:
        await message.answer("No miners yet.", reply_markup=menu_markup())
        return

    lines = ["Top Miners\n"]
    for index, player in enumerate(rows, start=1):
        lines.append(f"{index}. {player_title(player)} - {player['coins']} coins")
    await message.answer("\n".join(lines), reply_markup=menu_markup())


@dp.message(F.text == "Wallet")
async def wallet(message: Message) -> None:
    player = db.get_or_create_player(message.from_user)
    await message.answer(
        "Wallet\n\n"
        f"Game coins: {player['coins']}\n\n"
        "Top-ups and payments will be added after the core game loop is tested. "
        "For now, coins are in-game only.",
        reply_markup=menu_markup(),
    )


@dp.message(Command("admin_stats"))
async def admin_stats(message: Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Admin only.")
        return

    await message.answer(
        "Admin Stats\n\n"
        f"Players: {db.count_players()}\n"
        f"Total player coins: {db.total_coins()}"
    )


@dp.message(Command("grant"))
async def grant(message: Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Admin only.")
        return

    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("Usage: /grant <telegram_id> <amount>")
        return

    try:
        telegram_id = int(parts[1])
        amount = int(parts[2])
    except ValueError:
        await message.answer("telegram_id and amount must be numbers.")
        return

    if db.grant(telegram_id, amount):
        await message.answer(f"Granted {amount} coins to {telegram_id}.")
    else:
        await message.answer("Player not found.")


async def main() -> None:
    db.init()
    bot = Bot(config.bot_token)
    if config.mini_app_url:
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="Play BitCore Mine",
                web_app=WebAppInfo(url=config.mini_app_url),
            )
        )

    if config.use_webhook:
        if not config.public_base_url:
            raise RuntimeError("Webhook mode needs MINI_APP_URL or RENDER_EXTERNAL_URL")
        app = create_web_app(config, db)
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.webhook_path)
        setup_application(app, dp, bot=bot)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, config.webapp_host, config.webapp_port)
        await site.start()
        webhook_url = f"{config.public_base_url}{config.webhook_path}"
        await bot.set_webhook(webhook_url, drop_pending_updates=True)
        logging.info("Webhook is running at %s", webhook_url)
        logging.info("Mini App web server is running at %s", config.public_base_url)
        await asyncio.Event().wait()
        return

    await start_web_app(config, db)
    logging.info(
        "Mini App web server is running at http://%s:%s",
        config.webapp_host,
        config.webapp_port,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
