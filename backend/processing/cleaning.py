from __future__ import annotations

import re
from typing import Iterable, List

from backend.models import UnifiedSignal

WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(value: str) -> str:
    return WHITESPACE_RE.sub(" ", value or "").strip()


def clean_signals(signals: Iterable[UnifiedSignal]) -> List[UnifiedSignal]:
    cleaned: List[UnifiedSignal] = []
    seen = set()
    for signal in signals:
        signal.title = normalize_text(signal.title)
        signal.text = normalize_text(signal.text)
        dedupe_key = (
            signal.source,
            signal.region.lower(),
            signal.title.lower(),
            signal.text[:160].lower(),
        )
        if dedupe_key in seen or not signal.text:
            continue
        seen.add(dedupe_key)
        cleaned.append(signal)
    return cleaned
