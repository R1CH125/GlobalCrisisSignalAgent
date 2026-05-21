from __future__ import annotations

from typing import Dict, Iterable

from backend.models import CrisisIndicators, UnifiedSignal


def _category_average(signals: Iterable[UnifiedSignal], category: str) -> float:
    filtered = [signal.severity for signal in signals if signal.category == category]
    if not filtered:
        return 0.0
    return round(sum(filtered) / len(filtered), 3)


def score_components(
    signals: Iterable[UnifiedSignal],
    indicators: CrisisIndicators,
    historical_similarity: Dict[str, float],
) -> Dict[str, float]:
    social_score = _category_average(signals, "social")
    news_score = _category_average(signals, "news")
    environmental_score = _category_average(signals, "environmental")
    historical_score = max(historical_similarity.values(), default=0.0)

    boost = (
        0.1 * indicators.frequency_spike
        + 0.1 * indicators.multi_source_confirmation
        + 0.05 * indicators.environmental_correlation
    )

    return {
        "social_signals": min(social_score + boost, 1.0),
        "news_signals": min(news_score + boost, 1.0),
        "environmental_signals": min(environmental_score + boost, 1.0),
        "historical_similarity": historical_score,
    }


def compute_crisis_score(
    signals: Iterable[UnifiedSignal],
    indicators: CrisisIndicators,
    historical_similarity: Dict[str, float],
) -> Dict[str, float | str]:
    components = score_components(signals, indicators, historical_similarity)
    crisis_score = round(
        0.4 * components["environmental_signals"]
        + 0.3 * components["news_signals"]
        + 0.2 * components["social_signals"]
        + 0.1 * components["historical_similarity"],
        3,
    )
    return {
        **components,
        "crisis_score": crisis_score,
        "alert_level": classify_crisis_level(crisis_score),
    }


def classify_crisis_level(score: float) -> str:
    if score < 0.3:
        return "Normal"
    if score < 0.6:
        return "Emerging Risk"
    if score < 0.8:
        return "High Alert"
    return "Crisis Likely"
