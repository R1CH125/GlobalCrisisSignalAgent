from __future__ import annotations

from typing import List

from backend.data_sources.base import SourceClient
from backend.models import UnifiedSignal


class GDELTClient(SourceClient):
    source_name = "gdelt"
    category = "news"
    endpoint = "https://api.gdeltproject.org/api/v2/doc/doc"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode:
            region = self.config.tracked_regions[0]
            return [
                self.region_signal(
                    region,
                    title="Regional papers warn of livestock deaths",
                    text="GDELT-style article coverage points to prolonged drought and market stress in northern counties.",
                    keywords=["drought", "livestock deaths", "market stress"],
                    severity=0.81,
                    metadata={"source_type": "demo"},
                )
            ]

        data = self.request_json(
            self.endpoint,
            params={
                "query": " OR ".join(self.config.watch_terms[:6]),
                "maxrecords": 10,
                "format": "json",
            },
        )
        region = self.config.tracked_regions[0]
        return [
            self.region_signal(
                region,
                title=article.get("title", "GDELT article"),
                text=article.get("seendate", ""),
                keywords=self.config.watch_terms,
                severity=0.57,
                metadata={"raw": article},
            )
            for article in data.get("articles", [])
        ]


class NewsAPIClient(SourceClient):
    source_name = "newsapi"
    category = "news"
    endpoint = "https://newsapi.org/v2/everything"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode or not self.config.newsapi_key:
            region = self.config.tracked_regions[0]
            return [
                self.region_signal(
                    region,
                    title="Crop failure raises hunger fears",
                    text="Multiple local outlets report poor rains, failed crops, and rising malnutrition risks.",
                    keywords=["crop failure", "hunger", "malnutrition"],
                    severity=0.78,
                    metadata={"publisher": "demo-news"},
                )
            ]

        data = self.request_json(
            self.endpoint,
            headers={"X-Api-Key": self.config.newsapi_key},
            params={"q": " OR ".join(self.config.watch_terms[:6]), "language": "en", "pageSize": 10},
        )
        region = self.config.tracked_regions[0]
        return [
            self.region_signal(
                region,
                title=article.get("title", "NewsAPI article"),
                text=article.get("description") or article.get("content") or "",
                keywords=self.config.watch_terms,
                severity=0.56,
                metadata={"url": article.get("url")},
            )
            for article in data.get("articles", [])
        ]


class EventRegistryClient(SourceClient):
    source_name = "event_registry"
    category = "news"
    endpoint = "https://eventregistry.org/api/v1/article/getArticles"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode or not self.config.event_registry_api_key:
            region = self.config.tracked_regions[0]
            return [
                self.region_signal(
                    region,
                    title="Cross-border displacement concerns increase",
                    text="Regional coverage suggests livestock herders are moving earlier than usual because of water stress.",
                    keywords=["migration", "water stress", "displacement"],
                    severity=0.67,
                    metadata={"publisher": "event-registry-demo"},
                )
            ]

        data = self.request_json(
            self.endpoint,
            params={
                "apiKey": self.config.event_registry_api_key,
                "keyword": self.config.watch_terms[0],
                "articlesCount": 10,
            },
        )
        region = self.config.tracked_regions[0]
        results = data.get("articles", {}).get("results", [])
        return [
            self.region_signal(
                region,
                title=article.get("title", "Event Registry article"),
                text=article.get("body", ""),
                keywords=self.config.watch_terms,
                severity=0.55,
                metadata={"url": article.get("url")},
            )
            for article in results
        ]


class MediaStackClient(SourceClient):
    source_name = "mediastack"
    category = "news"
    endpoint = "http://api.mediastack.com/v1/news"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode or not self.config.mediastack_key:
            region = self.config.tracked_regions[0]
            return [
                self.region_signal(
                    region,
                    title="Commodity inflation follows drought",
                    text="Media tracking highlights food inflation and market shortages after weak rainy seasons.",
                    keywords=["food shortage", "inflation", "drought"],
                    severity=0.64,
                    metadata={"publisher": "mediastack-demo"},
                )
            ]

        data = self.request_json(
            self.endpoint,
            params={"access_key": self.config.mediastack_key, "keywords": ",".join(self.config.watch_terms[:6]), "limit": 10},
        )
        region = self.config.tracked_regions[0]
        return [
            self.region_signal(
                region,
                title=article.get("title", "MediaStack article"),
                text=article.get("description") or "",
                keywords=self.config.watch_terms,
                severity=0.54,
                metadata={"url": article.get("url")},
            )
            for article in data.get("data", [])
        ]
