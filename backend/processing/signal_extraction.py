from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Tuple

from backend.models import CrisisIndicators, UnifiedSignal

KEY_EVENT_LEXICON = {
    "water scarcity": ["dry wells", "water scarcity", "drought", "borehole failure", "rainfall deficit"],
    "food shortage": ["food shortage", "crop failure", "hunger", "famine", "livestock deaths", "malnutrition"],
    "migration": ["migration", "displacement", "families moving", "cross-border", "herders moving"],
    "disease": ["cholera", "malaria", "outbreak", "clinic overflow", "medicine shortage"],
    "infrastructure breakdown": ["power outage", "road collapse", "supply disruption", "health posts running short"],
}


def infer_key_events(signals: Iterable[UnifiedSignal]) -> Dict[str, int]:
    counts = Counter()
    for signal in signals:
        haystack = f"{signal.title} {signal.text} {' '.join(signal.keywords)}".lower()
        for event_name, terms in KEY_EVENT_LEXICON.items():
            if any(term in haystack for term in terms):
                counts[event_name] += 1
    return dict(counts)


def group_by_region(signals: Iterable[UnifiedSignal]) -> Dict[str, List[UnifiedSignal]]:
    grouped: Dict[str, List[UnifiedSignal]] = defaultdict(list)
    for signal in signals:
        grouped[signal.region].append(signal)
    return grouped


def compute_indicators(
    region: str,
    signals: List[UnifiedSignal],
    baseline_count: float,
    thresholds: Dict[str, float],
) -> CrisisIndicators:
    current_count = len(signals)
    baseline = max(baseline_count, 1.0)
    frequency_spike = min(current_count / baseline, 2.0) / 2.0
    categories = sorted({signal.category for signal in signals})
    multi_source_confirmation = min(len(categories) / thresholds["multi_source_min"], 1.0)
    geographic_clustering = min(current_count / 5.0, 1.0)
    has_environmental = any(signal.category == "environmental" for signal in signals)
    has_human = any(signal.category in {"social", "news"} for signal in signals)
    environmental_correlation = 1.0 if has_environmental and has_human else 0.25 if has_environmental else 0.0

    trigger_reasons: List[str] = []
    if current_count >= baseline * thresholds["keyword_spike_ratio"]:
        trigger_reasons.append(f"{region}: keyword volume spike above {thresholds['keyword_spike_ratio']:.1f}x baseline")
    if len(categories) >= thresholds["multi_source_min"]:
        trigger_reasons.append(f"{region}: multiple source categories confirm the same region")
    if has_environmental and any(signal.severity >= thresholds["environmental_anomaly"] for signal in signals):
        trigger_reasons.append(f"{region}: environmental anomaly exceeds {thresholds['environmental_anomaly']:.2f}")

    return CrisisIndicators(
        frequency_spike=frequency_spike,
        multi_source_confirmation=multi_source_confirmation,
        geographic_clustering=geographic_clustering,
        environmental_correlation=environmental_correlation,
        source_categories=categories,
        key_events=infer_key_events(signals),
        trigger_reasons=trigger_reasons,
    )


def summarize_region_signals(signals: List[UnifiedSignal]) -> Tuple[List[str], Dict[str, int]]:
    source_counts = Counter(signal.source for signal in signals)
    summary = [f"{signal.source}: {signal.title}" for signal in sorted(signals, key=lambda item: item.severity, reverse=True)[:5]]
    return summary, dict(source_counts)
