# BitCore Mine

Telegram game bot where players register, mine digital cores, collect coins, upgrade their rig, and climb the leaderboard.

## Setup

1. Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in your values:

```env
BOT_TOKEN=your_new_token_from_BotFather
ADMIN_IDS=your_telegram_id
DB_PATH=bitcore_mine.sqlite3
MINI_APP_URL=https://your-public-mini-app-url.example.com
WEBAPP_HOST=127.0.0.1
WEBAPP_PORT=8080
WEBAPP_DEV_USER_ID=your_telegram_id
```

You can find your Telegram ID with `@userinfobot` or `@getmyid_bot`.

4. Run the bot:

```powershell
python main.py
```

Or use the helper script:

```powershell
.\run_bot.ps1
```

## Player Commands

- `/start` - register and open the main menu
- `/menu` - main menu
- `/profile` - player profile
- `/mine` - mine status
- `/collect` - collect mined coins
- `/upgrades` - upgrade menu
- `/tasks` - daily tasks
- `/leaderboard` - top players

## Mini App

The bot now also serves a Telegram Mini App game screen at:

```text
http://127.0.0.1:8080/
```

For local browser testing, `WEBAPP_DEV_USER_ID` lets the app open without Telegram init data.

To show the Mini App button inside Telegram, publish this web app through a public HTTPS URL and put that URL into `MINI_APP_URL` in `.env`. Telegram clients need a public URL; `127.0.0.1` works only on your own computer, not inside other users' Telegram apps.

## Free Render Deploy

This repository includes `render.yaml` for a free Render Web Service.

Render settings:

```text
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

Environment variables to add in Render:

```env
BOT_TOKEN=your_new_token_from_BotFather
ADMIN_IDS=your_telegram_id
WEBAPP_DEV_USER_ID=
USE_WEBHOOK=true
```

On Render, the app automatically uses `RENDER_EXTERNAL_URL` as the Mini App URL and `PORT` as the server port. For local development, keep using `.env`.

Note: free Render services can sleep after inactivity, and the SQLite database on the free web service filesystem is not a production-grade persistent database. It is fine for early testing.

## Admin Commands

Admin access is controlled by `ADMIN_IDS` in `.env`.

- `/admin_stats` - show bot stats
- `/grant <telegram_id> <amount>` - add coins to a player
