from __future__ import annotations

from typing import Dict

import requests

from backend.models import CrisisReport


class ReliefWebAlert:
    """
    ReliefWeb's public API is primarily read-oriented. This integration uses it to
    enrich an alert payload with related reports, while still returning a concrete
    HTTP request pattern that can be wired into a partner submission workflow.
    """

    def __init__(self, api_url: str, enabled: bool = False):
        self.api_url = api_url
        self.enabled = enabled

    def send(self, report: CrisisReport) -> Dict[str, object]:
        payload = {
            "appname": "global-crisis-signal-agent",
            "query": {"value": report.region},
            "limit": 3,
        }
        related = []
        if self.enabled and self.api_url:
            response = requests.post(self.api_url, json=payload, timeout=10)
            if response.ok:
                related = response.json().get("data", [])
        return {
            "channel": "reliefweb",
            "payload": payload,
            "related_reports": related,
        }
