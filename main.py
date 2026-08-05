import sys
import argparse
from config_loader import load_config
from github_scraper import GitHubScraper
from evaluator import IssueEvaluator
from notifier import NotificationDispatcher

# Reconfigure console output to UTF-8 to prevent Windows emoji crashes
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="IssuePilot - Customizable Open-Source Issue Digest Agent")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to config YAML file")
    args = parser.parse_args()

    print("🚀 Starting IssuePilot Engine...")
    config = load_config(args.config)
    print(f"[Config] Target Tech Stack: {config.tech_stack}")
    print(f"[Config] Notification Channel: {config.notification_channel}")

    # 1. Scrape Issues
    print("\n--- [Step 1/3] Scraping Fresh Issues from GitHub ---")
    scraper = GitHubScraper()
    raw_issues = scraper.fetch_issues(config)
    print(f"Scraped {len(raw_issues)} raw open issues.")

    # 2. Evaluate & Rerank Issues
    print("\n--- [Step 2/3] Scoring & Reranking Issues ---")
    evaluator = IssueEvaluator()
    evaluated_issues = evaluator.evaluate_issues(raw_issues, config)
    print(f"Evaluated {len(evaluated_issues)} high-quality issues matching threshold ({config.min_score_threshold}/100).")

    # 3. Dispatch Notifications
    print("\n--- [Step 3/3] Delivering Daily Digest ---")
    dispatcher = NotificationDispatcher()
    dispatcher.dispatch(evaluated_issues, config)
    print("\n✅ IssuePilot Run Complete!")

if __name__ == "__main__":
    main()
