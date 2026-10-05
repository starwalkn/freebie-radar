# 🎮 Telegram Freebie & Deals Radar (24/7 Cloud Automated)

> Automated bot that continuously tracks 100% free games (100% OFF / Free to Keep) across Epic Games Store & Steam, broadcasting instant alerts to a Telegram Channel.

[![Freebie Radar 24/7 Auto Check](https://github.com/starwalkn/freebie-radar/actions/workflows/radar.yml/badge.svg)](https://github.com/starwalkn/freebie-radar/actions/workflows/radar.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## ⚡ How It Works
1. Runs serverless every 4 hours via **GitHub Actions** on Microsoft's cloud infrastructure.
2. Directly polls official **Epic Games** and **Steam** store promotions APIs.
3. Formats rich HTML Telegram messages featuring game posters, claim URLs, and deadline countdowns.
4. Auto-commits `posted_games_history.json` to prevent duplicate alerts.

---

## ⚙️ Configuration (GitHub Secrets)
To connect your own Telegram bot and channel:
1. Talk to `@BotFather` on Telegram -> `/newbot` -> get your `BOT_TOKEN`.
2. Create a public Telegram channel and add your bot as an **Administrator** with *Post Messages* permission.
3. In this GitHub repository, go to **Settings &rarr; Secrets and variables &rarr; Actions &rarr; New repository secret**:
   - `TG_BOT_TOKEN`: Your bot token from BotFather.
   - `TG_CHANNEL`: Your channel username (e.g. `@YourFreebieChannel`).

---

## 🛠️ Maintained by
Developed by NovaFortix Lab.  
Check out our suite of free tools at: **[Awesome Developer Utilities](https://github.com/starwalkn/awesome-developer-utilities)**
