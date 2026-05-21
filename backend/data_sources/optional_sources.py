from __future__ import annotations

from typing import List

from backend.data_sources.base import SourceClient
from backend.models import UnifiedSignal

try:
    from pytrends.request import TrendReq
except ImportError:  # pragma: no cover - dependency optional at runtime
    TrendReq = None


class GoogleTrendsClient(SourceClient):
    source_name = "google_trends"
    category = "social"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode or TrendReq is None:
            return []

        trend = TrendReq(hl="en-US", tz=360)
        keywords = self.config.watch_terms[:5]
        trend.build_payload(keywords, timeframe="now 7-d")
        interest = trend.interest_over_time()
        if interest.empty:
            return []

        region = self.config.tracked_regions[0]
        return [
            self.region_signal(
                region,
                title="Google Trends spike",
                text=f"Recent search interest increased for {keyword}.",
                keywords=[keyword],
                severity=0.52,
                metadata={"peak_interest": int(interest[keyword].max())},
            )
            for keyword in keywords
        ]


class FAOSTATClient(SourceClient):
    source_name = "faostat"
    category = "news"
    endpoint = "https://fenixservices.fao.org/faostat/api/v1/en"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode:
            return []

        data = self.request_json(f"{self.endpoint}/data/FS")
        region = self.config.tracked_regions[0]
        return [
            self.region_signal(
                region,
                title="FAOSTAT agricultural signal",
                text=f"Commodity indicator {item.get('item')}",
                keywords=["agriculture", "food systems"],
                severity=0.45,
                metadata={"raw": item},
            )
            for item in data.get("data", [])[:5]
        ]
