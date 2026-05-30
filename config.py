from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_ids: set[int]
    db_path: str
    mini_app_url: str
    public_base_url: str
    webapp_host: str
    webapp_port: int
    webapp_dev_user_id: int | None
    use_webhook: bool
    webhook_path: str


def load_config() -> Config:
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token or bot_token == "put_your_new_bot_token_here":
        raise RuntimeError("BOT_TOKEN is missing. Add your new BotFather token to .env")

    admin_ids_raw = os.getenv("ADMIN_IDS", "").strip()
    admin_ids: set[int] = set()
    if admin_ids_raw:
        admin_ids = {
            int(value.strip())
            for value in admin_ids_raw.split(",")
            if value.strip()
        }

    render_url = os.getenv("RENDER_EXTERNAL_URL", "").strip()
    mini_app_url = os.getenv("MINI_APP_URL", "").strip() or render_url
    is_render = os.getenv("RENDER", "").strip().lower() == "true"
    use_webhook_raw = os.getenv("USE_WEBHOOK", "").strip().lower()
    use_webhook = (
        use_webhook_raw in {"1", "true", "yes", "on"}
        if use_webhook_raw
        else bool(is_render and mini_app_url)
    )

    return Config(
        bot_token=bot_token,
        admin_ids=admin_ids,
        db_path=os.getenv("DB_PATH", "bitcore_mine.sqlite3").strip(),
        mini_app_url=mini_app_url,
        public_base_url=mini_app_url.rstrip("/"),
        webapp_host=os.getenv("WEBAPP_HOST", "0.0.0.0" if is_render else "127.0.0.1").strip(),
        webapp_port=int(os.getenv("PORT", os.getenv("WEBAPP_PORT", "8080"))),
        webapp_dev_user_id=(
            int(os.getenv("WEBAPP_DEV_USER_ID", "0"))
            if os.getenv("WEBAPP_DEV_USER_ID", "0").strip()
            else None
        )
        or None,
        use_webhook=use_webhook,
        webhook_path=os.getenv("WEBHOOK_PATH", "/telegram/webhook").strip() or "/telegram/webhook",
    )
