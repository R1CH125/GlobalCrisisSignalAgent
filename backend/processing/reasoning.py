from __future__ import annotations

from typing import Dict, List

import requests

from backend.config import AppConfig
from backend.models import CrisisIndicators, UnifiedSignal


class NemotronReasoner:
    def __init__(self, config: AppConfig):
        self.config = config

    def build_key_event_prompt(self, region: str, signals: List[UnifiedSignal]) -> str:
        signal_lines = "\n".join(f"- [{signal.category}] {signal.title}: {signal.text}" for signal in signals[:8])
        return (
            "You are Nemotron Core, a humanitarian early warning analyst.\n"
            "Extract key events from the region below. Focus on scarcity, migration, disease, and infrastructure breakdown.\n"
            f"Region: {region}\nSignals:\n{signal_lines}\n"
            "Return JSON with key_events and evidence."
        )

    def build_indicator_prompt(self, region: str, indicators: CrisisIndicators) -> str:
        return (
            "Assess crisis indicators for the region below and return JSON.\n"
            f"Region: {region}\n"
            f"Frequency spike: {indicators.frequency_spike}\n"
            f"Multi-source confirmation: {indicators.multi_source_confirmation}\n"
            f"Geographic clustering: {indicators.geographic_clustering}\n"
            f"Environmental correlation: {indicators.environmental_correlation}\n"
        )

    def build_synthesis_prompt(
        self,
        region: str,
        signals: List[UnifiedSignal],
        indicators: CrisisIndicators,
        historical_similarity: Dict[str, float],
    ) -> str:
        return (
            "Synthesize social, news, and environmental signals into a structured crisis assessment.\n"
            f"Region: {region}\n"
            f"Indicators: {indicators.to_dict()}\n"
            f"Historical similarity: {historical_similarity}\n"
            f"Top evidence: {[signal.title for signal in signals[:5]]}\n"
            "Return JSON with crisis_type, signals, confidence, and reasoning."
        )

    def analyze(
        self,
        region: str,
        country: str,
        signals: List[UnifiedSignal],
        indicators: CrisisIndicators,
        historical_similarity: Dict[str, float],
    ) -> Dict[str, object]:
        if self.config.nemotron_api_url and self.config.nemotron_api_key:
            payload = {
                "model": self.config.nemotron_model,
                "messages": [
                    {"role": "system", "content": "You are Nemotron Core, a humanitarian crisis analyst."},
                    {
                        "role": "user",
                        "content": self.build_synthesis_prompt(region, signals, indicators, historical_similarity),
                    },
                ],
            }
            response = requests.post(
                self.config.nemotron_api_url,
                headers={
                    "Authorization": f"Bearer {self.config.nemotron_api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
            message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {
                "region": region,
                "country": country,
                "raw_model_output": message,
                "prompt": self.build_synthesis_prompt(region, signals, indicators, historical_similarity),
            }

        return self.local_reason(region, country, signals, indicators, historical_similarity)

    def local_reason(
        self,
        region: str,
        country: str,
        signals: List[UnifiedSignal],
        indicators: CrisisIndicators,
        historical_similarity: Dict[str, float],
    ) -> Dict[str, object]:
        evidence = [signal.title for signal in sorted(signals, key=lambda item: item.severity, reverse=True)[:5]]
        crisis_type = []
        key_events = indicators.key_events
        if key_events.get("water scarcity") or max(historical_similarity, key=historical_similarity.get) == "drought":
            crisis_type.append("water scarcity")
        if key_events.get("food shortage"):
            crisis_type.append("food shortage")
        if key_events.get("migration"):
            crisis_type.append("displacement risk")
        if key_events.get("disease"):
            crisis_type.append("disease pressure")
        if key_events.get("infrastructure breakdown"):
            crisis_type.append("infrastructure breakdown")
        if not crisis_type:
            crisis_type.append("multi-factor humanitarian stress")

        confidence = round(
            min(
                1.0,
                (
                    indicators.frequency_spike
                    + indicators.multi_source_confirmation
                    + indicators.geographic_clustering
                    + indicators.environmental_correlation
                )
                / 4.0,
            ),
            2,
        )
        return {
            "region": region,
            "country": country,
            "crisis_type": crisis_type,
            "signals": evidence,
            "confidence": confidence,
            "key_events": key_events,
            "indicator_assessment": indicators.to_dict(),
            "historical_similarity": historical_similarity,
            "prompt_preview": self.build_synthesis_prompt(region, signals, indicators, historical_similarity),
        }
