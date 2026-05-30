from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

from game import UPGRADES


def main_menu(mini_app_url: str = "") -> ReplyKeyboardMarkup:
    keyboard: list[list[KeyboardButton]] = []
    if mini_app_url:
        keyboard.append([KeyboardButton(text="Play BitCore Mine", web_app=WebAppInfo(url=mini_app_url))])

    keyboard.extend(
        [
            [KeyboardButton(text="Mine"), KeyboardButton(text="Collect")],
            [KeyboardButton(text="Upgrades"), KeyboardButton(text="Profile")],
            [KeyboardButton(text="Tasks"), KeyboardButton(text="Leaderboard")],
            [KeyboardButton(text="Wallet")],
        ]
    )

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def launch_app_button(mini_app_url: str) -> InlineKeyboardMarkup | None:
    if not mini_app_url:
        return None
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Open Mini Game",
                    web_app=WebAppInfo(url=mini_app_url),
                )
            ]
        ]
    )


def upgrades_menu(levels: dict[str, int]) -> InlineKeyboardMarkup:
    buttons = []
    for key, upgrade in UPGRADES.items():
        current_level = levels[key]
        cost = upgrade.cost(current_level)
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{upgrade.emoji} {upgrade.title} Lv.{current_level} - {cost} coins",
                    callback_data=f"upgrade:{key}",
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)
