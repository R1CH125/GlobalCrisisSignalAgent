from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

from backend.config import AppConfig, RegionConfig
from backend.models import UnifiedSignal


class SourceClient:
    source_name = "source"
    category = "unknown"

    def __init__(self, config: AppConfig):
        self.config = config

    def fetch(self) -> List[UnifiedSignal]:
        raise NotImplementedError

    def request_json(
        self,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 15,
    ) -> Dict[str, Any]:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()

    def build_signal(
        self,
        *,
        title: str,
        text: str,
        region: str,
        country: str,
        latitude: float,
        longitude: float,
        keywords: List[str],
        severity: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UnifiedSignal:
        return UnifiedSignal(
            source=self.source_name,
            category=self.category,
            title=title,
            text=text,
            region=region,
            country=country,
            latitude=latitude,
            longitude=longitude,
            keywords=keywords,
            severity=max(0.0, min(severity, 1.0)),
            metadata=metadata or {},
        )

    def region_signal(
        self,
        region: RegionConfig,
        *,
        title: str,
        text: str,
        keywords: List[str],
        severity: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UnifiedSignal:
        return self.build_signal(
            title=title,
            text=text,
            region=region.name,
            country=region.country,
            latitude=region.latitude,
            longitude=region.longitude,
            keywords=keywords,
            severity=severity,
            metadata=metadata,
        )
