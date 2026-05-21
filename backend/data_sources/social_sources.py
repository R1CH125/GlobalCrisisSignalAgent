from __future__ import annotations

from typing import List

from backend.data_sources.base import SourceClient
from backend.models import UnifiedSignal

try:
    import praw
except ImportError:  # pragma: no cover - dependency optional at runtime
    praw = None


class TwitterClient(SourceClient):
    source_name = "twitter"
    category = "social"
    endpoint = "https://api.twitter.com/2/tweets/search/recent"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode or not self.config.twitter_bearer_token:
            region = self.config.tracked_regions[0]
            return [
                self.region_signal(
                    region,
                    title="Residents report dry wells and food queues",
                    text="Community posts mention dry wells, livestock losses, and rising maize prices in Northern Kenya.",
                    keywords=["dry wells", "food shortage", "livestock deaths"],
                    severity=0.82,
                    metadata={"engagement": 219, "query": "Northern Kenya drought food shortage"},
                ),
                self.region_signal(
                    region,
                    title="Aid workers mention migration from arid counties",
                    text="Recent social chatter points to families moving after repeated borehole failures.",
                    keywords=["migration", "water scarcity", "borehole failure"],
                    severity=0.76,
                    metadata={"engagement": 147, "query": "Kenya migration drought"},
                ),
            ]

        query = " OR ".join(f'"{term}"' for term in self.config.watch_terms[:6])
        data = self.request_json(
            self.endpoint,
            headers={"Authorization": f"Bearer {self.config.twitter_bearer_token}"},
            params={
                "query": query,
                "max_results": 10,
                "tweet.fields": "created_at,lang,geo,public_metrics",
            },
        )
        region = self.config.tracked_regions[0]
        return [
            self.region_signal(
                region,
                title="Twitter signal",
                text=tweet.get("text", ""),
                keywords=self.config.watch_terms,
                severity=0.6,
                metadata={"tweet_id": tweet.get("id"), "raw": tweet},
            )
            for tweet in data.get("data", [])
        ]


class RedditClient(SourceClient):
    source_name = "reddit"
    category = "social"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode or not all(
            [self.config.reddit_client_id, self.config.reddit_client_secret, praw]
        ):
            region = self.config.tracked_regions[0]
            return [
                self.region_signal(
                    region,
                    title="Reddit post tracks failed harvests",
                    text="Discussion threads reference crop failure, cattle deaths, and a lack of market supplies.",
                    keywords=["crop failure", "food shortage", "livestock deaths"],
                    severity=0.7,
                    metadata={"subreddit": "worldnews"},
                )
            ]

        reddit = praw.Reddit(
            client_id=self.config.reddit_client_id,
            client_secret=self.config.reddit_client_secret,
            user_agent=self.config.reddit_user_agent,
        )
        signals: List[UnifiedSignal] = []
        region = self.config.tracked_regions[0]
        for submission in reddit.subreddit("worldnews+news+climate").search(
            " OR ".join(self.config.watch_terms[:6]), sort="new", limit=8
        ):
            signals.append(
                self.region_signal(
                    region,
                    title=submission.title,
                    text=submission.selftext or submission.title,
                    keywords=self.config.watch_terms,
                    severity=0.58,
                    metadata={"url": submission.url, "score": submission.score},
                )
            )
        return signals


class TelegramClient(SourceClient):
    source_name = "telegram"
    category = "social"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode or not self.config.telegram_bot_token:
            region = self.config.tracked_regions[0]
            return [
                self.region_signal(
                    region,
                    title="Telegram field report",
                    text="Local channel reports water trucking demand increasing and health posts running short on supplies.",
                    keywords=["water scarcity", "medicine shortage", "field report"],
                    severity=0.73,
                    metadata={"channel": "@field_update"},
                )
            ]

        data = self.request_json(
            f"https://api.telegram.org/bot{self.config.telegram_bot_token}/getUpdates"
        )
        region = self.config.tracked_regions[0]
        signals: List[UnifiedSignal] = []
        for update in data.get("result", []):
            message = update.get("message", {})
            chat_id = str(message.get("chat", {}).get("id", ""))
            if self.config.telegram_chat_ids and chat_id not in self.config.telegram_chat_ids:
                continue
            text = message.get("text", "")
            if not text:
                continue
            signals.append(
                self.region_signal(
                    region,
                    title="Telegram update",
                    text=text,
                    keywords=self.config.watch_terms,
                    severity=0.55,
                    metadata={"update_id": update.get("update_id"), "chat_id": chat_id},
                )
            )
        return signals
