import os
import yaml
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class AppConfig(BaseModel):
    tech_stack: List[str]
    target_repos: List[str] = []
    max_daily_issues: int = 3
    min_score_threshold: int = 50
    search_labels: List[str] = ["good first issue"]
    notification_channel: str = "telegram"

def load_config(config_path: str = "config.yaml") -> AppConfig:
    """Load configuration from config.yaml with environment overrides."""
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}

    # Environment variable overrides
    env_stack = os.getenv("USER_TECH_STACK")
    if env_stack:
        data["tech_stack"] = [s.strip().lower() for s in env_stack.split(",") if s.strip()]

    env_channel = os.getenv("NOTIFICATION_CHANNEL")
    if env_channel:
        data["notification_channel"] = env_channel.strip().lower()

    return AppConfig(**data)
