from __future__ import annotations

import math
from typing import Dict

from backend.models import CrisisIndicators

ARCHETYPES = {
    "drought": [1.0, 0.8, 0.7, 1.0],
    "displacement": [0.7, 0.9, 0.6, 0.5],
    "outbreak": [0.6, 0.8, 0.5, 0.4],
    "infrastructure": [0.5, 0.7, 0.8, 0.3],
}


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


def compute_historical_similarity(indicators: CrisisIndicators) -> Dict[str, float]:
    vector = [
        indicators.frequency_spike,
        indicators.multi_source_confirmation,
        indicators.geographic_clustering,
        indicators.environmental_correlation,
    ]
    scores = {
        name: round(cosine_similarity(vector, prototype), 3)
        for name, prototype in ARCHETYPES.items()
    }
    return scores
