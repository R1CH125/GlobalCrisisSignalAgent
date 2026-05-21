from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class UnifiedSignal:
    source: str
    category: str
    title: str
    text: str
    region: str
    country: str
    latitude: float
    longitude: float
    timestamp: str = field(default_factory=utcnow_iso)
    keywords: List[str] = field(default_factory=list)
    severity: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CrisisIndicators:
    frequency_spike: float
    multi_source_confirmation: float
    geographic_clustering: float
    environmental_correlation: float
    source_categories: List[str]
    key_events: Dict[str, int]
    trigger_reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CrisisReport:
    region: str
    country: str
    latitude: float
    longitude: float
    crisis_type: List[str]
    signals: List[str]
    confidence: float
    crisis_score: float
    alert_level: str
    created_at: str
    source_counts: Dict[str, int]
    indicators: Dict[str, Any]
    reasoning: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
