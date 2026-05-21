from __future__ import annotations

from typing import Dict

import boto3

from backend.models import CrisisReport


class SESEmailAlert:
    def __init__(self, sender_email: str, recipient_email: str, region_name: str):
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        self.region_name = region_name

    def send(self, report: CrisisReport) -> Dict[str, object]:
        subject = f"{report.alert_level}: {report.region} crisis score {report.crisis_score}"
        body = (
            f"Region: {report.region}, {report.country}\n"
            f"Crisis score: {report.crisis_score}\n"
            f"Crisis types: {', '.join(report.crisis_type)}\n"
            f"Signals:\n- " + "\n- ".join(report.signals[:5])
        )
        if self.sender_email and self.recipient_email:
            client = boto3.client("ses", region_name=self.region_name)
            client.send_email(
                Source=self.sender_email,
                Destination={"ToAddresses": [self.recipient_email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": body}},
                },
            )
        return {"channel": "ses_email", "subject": subject, "body": body}
