from __future__ import annotations

from typing import Dict

import requests

from backend.models import CrisisReport


def build_alert_payload(report: CrisisReport) -> Dict[str, object]:
    return {
        "region": report.region,
        "country": report.country,
        "alert_level": report.alert_level,
        "crisis_score": report.crisis_score,
        "crisis_type": report.crisis_type,
        "signals": report.signals,
        "reasoning": report.reasoning,
        "created_at": report.created_at,
    }


class SlackWebhookAlert:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, report: CrisisReport) -> Dict[str, object]:
        payload = {
            "text": f"[{report.alert_level}] {report.region} crisis score={report.crisis_score}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"*{report.region}, {report.country}*\n"
                            f"Score: `{report.crisis_score}`\n"
                            f"Signals: {', '.join(report.signals[:3])}"
                        ),
                    },
                }
            ],
        }
        if self.webhook_url:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
        return {"channel": "slack", "payload": payload}


class DiscordWebhookAlert:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, report: CrisisReport) -> Dict[str, object]:
        payload = {
            "content": f"Global Crisis Signal Agent: {report.region} moved to {report.alert_level}",
            "embeds": [
                {
                    "title": f"{report.region} | score {report.crisis_score}",
                    "description": "\n".join(report.signals[:4]),
                    "color": 15158332 if report.crisis_score >= 0.8 else 16763904,
                }
            ],
        }
        if self.webhook_url:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
        return {"channel": "discord", "payload": payload}


class NGOWebhookAlert:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, report: CrisisReport) -> Dict[str, object]:
        payload = build_alert_payload(report)
        if self.webhook_url:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
        return {"channel": "ngo_webhook", "payload": payload}
