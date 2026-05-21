from __future__ import annotations

from typing import Dict, List

from backend.alerts.reliefweb import ReliefWebAlert
from backend.alerts.ses_email import SESEmailAlert
from backend.alerts.webhooks import DiscordWebhookAlert, NGOWebhookAlert, SlackWebhookAlert
from backend.config import AppConfig
from backend.models import CrisisReport


class AlertDispatcher:
    def __init__(self, config: AppConfig):
        self.handlers = [
            ReliefWebAlert(config.reliefweb_api_url, enabled=config.enable_reliefweb_lookup),
            SlackWebhookAlert(config.slack_webhook_url),
            DiscordWebhookAlert(config.discord_webhook_url),
            SESEmailAlert(config.ses_sender_email, config.ses_recipient_email, config.aws_region),
            NGOWebhookAlert(config.ngo_webhook_url),
        ]

    def dispatch(self, report: CrisisReport) -> List[Dict[str, object]]:
        results = []
        for handler in self.handlers:
            try:
                results.append(handler.send(report))
            except Exception as exc:  # pragma: no cover - network dependent
                results.append({"channel": handler.__class__.__name__, "error": str(exc)})
        return results
