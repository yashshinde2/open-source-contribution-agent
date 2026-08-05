import os
import requests
from typing import List
from models import Issue
from config_loader import AppConfig

class NotificationDispatcher:
    """Dispatches formatted issue digests to Telegram, Discord, or Console."""

    def dispatch(self, issues: List[Issue], config: AppConfig):
        top_issues = issues[:config.max_daily_issues]
        channel = config.notification_channel.lower()

        if not top_issues:
            print("[Info] No issues met the score threshold today.")
            return

        if channel == "telegram":
            self._send_telegram(top_issues)
        elif channel == "discord":
            self._send_discord(top_issues)
        else:
            self._send_console(top_issues)

    def _send_telegram(self, issues: List[Issue]):
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not token or not chat_id:
            print("[Warning] Telegram credentials missing. Printing to console instead:")
            self._send_console(issues)
            return

        clean_token = token.strip()
        if clean_token.lower().startswith("bot"):
            clean_token = clean_token[3:]

        lines = [
            "📬 <b>Your Daily Custom Open-Source Issue Digest</b>\n",
            "Here are fresh, top-scoring issues tailored to your tech stack:\n"
        ]

        for i, issue in enumerate(issues, 1):
            title = issue.title.replace("<", "&lt;").replace(">", "&gt;")
            url = issue.url
            repo = issue.repository or "GitHub"
            stack = ", ".join(issue.tech_stack)
            score = issue.score

            lines.append(f"<b>{i}. 📌 {title}</b>")
            lines.append(f"🏢 <b>Repo:</b> {repo}")
            lines.append(f"💻 <b>Tech Stack:</b> {stack} | <b>Score:</b> {score}/100")
            lines.append(f"🔗 <a href='{url}'>Tackle this issue on GitHub</a>\n")

        lines.append("💡 <i>Comment on the issue asking maintainers to assign it to you before starting work!</i>")
        message_text = "\n".join(lines)

        url = f"https://api.telegram.org/bot{clean_token}/sendMessage"
        payload = {
            "chat_id": chat_id.strip(),
            "text": message_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }

        try:
            res = requests.post(url, json=payload, timeout=10)
            if res.status_code == 200:
                print("Successfully sent daily digest to Telegram!")
            else:
                print(f"Telegram API Error ({res.status_code}): {res.text}")
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")

    def _send_discord(self, issues: List[Issue]):
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        if not webhook_url:
            print("[Warning] DISCORD_WEBHOOK_URL missing. Printing to console instead:")
            self._send_console(issues)
            return

        embeds = []
        for issue in issues:
            embeds.append({
                "title": f"📌 {issue.title}",
                "url": issue.url,
                "description": f"🏢 **Repo**: `{issue.repository}`\n💻 **Tech Stack**: `{', '.join(issue.tech_stack)}` | **Score**: `{issue.score}/100`",
                "color": 3066993
            })

        payload = {
            "content": "📬 **Your Daily Custom Open-Source Issue Digest**",
            "embeds": embeds
        }

        try:
            res = requests.post(webhook_url, json=payload, timeout=10)
            if res.status_code in (200, 204):
                print("Successfully sent daily digest to Discord!")
            else:
                print(f"Discord Webhook Error ({res.status_code}): {res.text}")
        except Exception as e:
            print(f"Failed to send Discord message: {e}")

    def _send_console(self, issues: List[Issue]):
        print("\n" + "=" * 60)
        print("📬 YOUR DAILY CUSTOM OPEN-SOURCE ISSUE DIGEST")
        print("=" * 60)
        for i, issue in enumerate(issues, 1):
            print(f"{i}. 📌 {issue.title}")
            print(f"   🏢 Repo: {issue.repository}")
            print(f"   💻 Tech Stack: {', '.join(issue.tech_stack)} | Score: {issue.score}/100")
            print(f"   🔗 Link: {issue.url}\n")
        print("=" * 60)
