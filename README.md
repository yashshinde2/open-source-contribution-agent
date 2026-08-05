# ⚡ IssuePilot: Custom Open-Source Issue Digest Agent

**IssuePilot** is a zero-database, highly customizable open-source issue digest engine. It continuously discovers, evaluates, and delivers **fresh, beginner-friendly GitHub issues** tailored specifically to **your preferred tech stack** directly to your **Telegram, Discord, or Console**.

---

## ✨ Why IssuePilot?

- ⚡ **Zero Database Required**: 100% lightweight state-free execution. No MongoDB setup needed!
- 🕒 **Time-Window Duplicate Prevention**: Queries issues created within a configurable date window (`created:>={YYYY-MM-DD}`), preventing duplicate alerts without storing data in a database.
- 🎯 **Custom Tech Stack Configuration**: Simply type your favorite technologies into `config.yaml` (`python`, `django`, `react`, `rust`, `golang`, `flutter`, `docker`, etc.).
- 🔄 **Fresh Issue Search**: Queries open GitHub issues sorted by creation date descending (`sort="created", direction="desc"`) so you get active, recent tasks.
- 📱 **Multi-Channel Alerts**: Supports **Telegram Bot**, **Discord Webhook**, or **Console Output**.
- ☁️ **1-Click 2-Minute Setup**: Fork the repo, add your Telegram/Discord credentials to GitHub Secrets, and enjoy daily issue alerts automatically for free!

---

## 🛠️ How It Works

```
┌───────────────────────────┐
│     1. User Config        │ ➔ User defines tech_stack, date window & notification channel
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│     2. GitHub Scraper     │ ➔ Pulls fresh issues matching created:>={YYYY-MM-DD}
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│    3. Dynamic Evaluator   │ ➔ Scores 1-100 & reranks issues against user's custom stack
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│   4. Daily Dispatcher     │ ➔ Delivers top 3 custom issues straight to Telegram/Discord
└───────────────────────────┘
```

---

## ⚙️ Quick Start (2-Minute Setup)

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/YOUR_USERNAME/issue-pilot.git
cd issue-pilot
pip install -r requirements.txt
```

### 2. Customize `config.yaml`
Edit `config.yaml` to specify your preferred tech stack and delivery channel:

```yaml
# Add your favorite tech stacks!
tech_stack:
  - "python"
  - "django"
  - "react"
  - "typescript"

# Time-window date filter (Prevents duplicate alerts!)
created_within_days: 30
difficulty_preference: "beginner"

# Target specific repos or leave [] to search all of GitHub
target_repos: []

# Options: "telegram", "discord", or "console"
notification_channel: "telegram"
```

### 3. Run Locally
```bash
python main.py
```

---

## ☁️ Automated GitHub Actions Setup (Zero Cost)

1. Fork this repository on GitHub.
2. Go to **Settings ➔ Secrets and variables ➔ Actions**.
3. Add your secrets:
   - `TELEGRAM_BOT_TOKEN` *(from @BotFather)*
   - `TELEGRAM_CHAT_ID` *(from @userinfobot)*
   - `DISCORD_WEBHOOK_URL` *(Optional for Discord)*

The GitHub Actions workflow will run automatically every day at `06:00 UTC` and deliver fresh issues tailored to your tech stack straight to your phone!

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
