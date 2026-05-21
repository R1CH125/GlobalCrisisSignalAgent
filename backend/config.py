from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List

from dotenv import load_dotenv

load_dotenv()


@dataclass
class RegionConfig:
    name: str
    country: str
    latitude: float
    longitude: float


@dataclass
class AppConfig:
    demo_mode: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
    monitor_interval_seconds: int = int(os.getenv("MONITOR_INTERVAL_SECONDS", "60"))
    history_window: int = int(os.getenv("HISTORY_WINDOW", "20"))
    twitter_bearer_token: str = os.getenv("TWITTER_BEARER_TOKEN", "")
    newsapi_key: str = os.getenv("NEWSAPI_KEY", "")
    event_registry_api_key: str = os.getenv("EVENT_REGISTRY_API_KEY", "")
    mediastack_key: str = os.getenv("MEDIASTACK_KEY", "")
    openweather_key: str = os.getenv("OPENWEATHER_KEY", "")
    noaa_token: str = os.getenv("NOAA_TOKEN", "")
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_ids: List[str] = field(
        default_factory=lambda: [value.strip() for value in os.getenv("TELEGRAM_CHAT_IDS", "").split(",") if value.strip()]
    )
    reddit_client_id: str = os.getenv("REDDIT_CLIENT_ID", "")
    reddit_client_secret: str = os.getenv("REDDIT_CLIENT_SECRET", "")
    reddit_user_agent: str = os.getenv("REDDIT_USER_AGENT", "global-crisis-signal-agent")
    slack_webhook_url: str = os.getenv("SLACK_WEBHOOK_URL", "")
    discord_webhook_url: str = os.getenv("DISCORD_WEBHOOK_URL", "")
    ngo_webhook_url: str = os.getenv("NGO_WEBHOOK_URL", "")
    reliefweb_api_url: str = os.getenv("RELIEFWEB_API_URL", "https://api.reliefweb.int/v1/reports")
    enable_reliefweb_lookup: bool = os.getenv("ENABLE_RELIEFWEB_LOOKUP", "false").lower() == "true"
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    ses_sender_email: str = os.getenv("SES_SENDER_EMAIL", "")
    ses_recipient_email: str = os.getenv("SES_RECIPIENT_EMAIL", "")
    nemotron_api_url: str = os.getenv("NEMOTRON_API_URL", "")
    nemotron_api_key: str = os.getenv("NEMOTRON_API_KEY", "")
    nemotron_model: str = os.getenv("NEMOTRON_MODEL", "nemotron")
    gfms_api_url: str = os.getenv("GFMS_API_URL", "")
    copernicus_api_url: str = os.getenv("COPERNICUS_API_URL", "")
    nasa_earthdata_url: str = os.getenv(
        "NASA_EARTHDATA_URL",
        "https://cmr.earthdata.nasa.gov/search/granules.json",
    )
    watch_terms: List[str] = field(
        default_factory=lambda: [
            "drought",
            "food shortage",
            "famine",
            "migration",
            "cholera",
            "malaria",
            "flooding",
            "dry wells",
            "crop failure",
            "power outage",
            "medicine shortage",
        ]
    )
    tracked_regions: List[RegionConfig] = field(
        default_factory=lambda: [
            RegionConfig("Northern Kenya", "Kenya", 3.52, 37.62),
            RegionConfig("Horn of Africa", "Regional", 8.98, 39.90),
            RegionConfig("Bangladesh Delta", "Bangladesh", 23.70, 90.35),
            RegionConfig("Sudan", "Sudan", 15.50, 32.56),
            RegionConfig("Haiti", "Haiti", 18.59, -72.31),
        ]
    )
    thresholds: Dict[str, float] = field(
        default_factory=lambda: {
            "keyword_spike_ratio": 1.2,
            "multi_source_min": 2.0,
            "environmental_anomaly": 0.65,
            "report_trigger": 0.35,
        }
    )


def get_config() -> AppConfig:
    return AppConfig()
