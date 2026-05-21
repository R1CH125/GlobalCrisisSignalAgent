from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timezone
from threading import Event, Thread
from typing import Deque, Dict, List

from backend.alerts.dispatcher import AlertDispatcher
from backend.config import AppConfig
from backend.data_sources import (
    CopernicusClimateClient,
    EventRegistryClient,
    FAOSTATClient,
    GDELTClient,
    GlobalFloodMonitoringClient,
    GoogleTrendsClient,
    MediaStackClient,
    NASAEarthDataClient,
    NOAAClimateClient,
    NewsAPIClient,
    OpenWeatherClient,
    RedditClient,
    TelegramClient,
    TwitterClient,
)
from backend.demo import build_demo_signals
from backend.models import CrisisReport, UnifiedSignal
from backend.processing.cleaning import clean_signals
from backend.processing.historical_similarity import compute_historical_similarity
from backend.processing.reasoning import NemotronReasoner
from backend.processing.signal_extraction import compute_indicators, group_by_region, summarize_region_signals
from backend.scoring.crisis_score import compute_crisis_score


class CrisisSignalAgent:
    def __init__(self, config: AppConfig):
        self.config = config
        self.reasoner = NemotronReasoner(config)
        self.dispatcher = AlertDispatcher(config)
        self.clients = [
            TwitterClient(config),
            RedditClient(config),
            TelegramClient(config),
            GDELTClient(config),
            NewsAPIClient(config),
            EventRegistryClient(config),
            MediaStackClient(config),
            OpenWeatherClient(config),
            NASAEarthDataClient(config),
            NOAAClimateClient(config),
            GlobalFloodMonitoringClient(config),
            CopernicusClimateClient(config),
            GoogleTrendsClient(config),
            FAOSTATClient(config),
        ]
        self.reports: Deque[CrisisReport] = deque(maxlen=30)
        self.alert_log: Deque[Dict[str, object]] = deque(maxlen=60)
        self.baselines: Dict[str, float] = defaultdict(lambda: 2.0)
        self.source_health: Dict[str, str] = {}
        self._stop_event = Event()
        self._thread: Thread | None = None

    def collect_signals(self) -> List[UnifiedSignal]:
        signals: List[UnifiedSignal] = []
        for client in self.clients:
            try:
                batch = client.fetch()
                signals.extend(batch)
                self.source_health[client.source_name] = f"ok ({len(batch)})"
            except Exception as exc:  # pragma: no cover - network dependent
                self.source_health[client.source_name] = f"error: {exc}"
        return clean_signals(signals)

    def analyze_signals(self, signals: List[UnifiedSignal]) -> List[CrisisReport]:
        reports: List[CrisisReport] = []
        for region, region_signals in group_by_region(signals).items():
            indicators = compute_indicators(
                region,
                region_signals,
                baseline_count=self.baselines[region],
                thresholds=self.config.thresholds,
            )
            historical_similarity = compute_historical_similarity(indicators)
            score_result = compute_crisis_score(region_signals, indicators, historical_similarity)
            if score_result["crisis_score"] < self.config.thresholds["report_trigger"]:
                self.baselines[region] = (self.baselines[region] * 0.7) + (len(region_signals) * 0.3)
                continue

            sample = region_signals[0]
            reasoning = self.reasoner.analyze(
                region,
                sample.country,
                region_signals,
                indicators,
                historical_similarity,
            )
            summaries, source_counts = summarize_region_signals(region_signals)
            report = CrisisReport(
                region=region,
                country=sample.country,
                latitude=sample.latitude,
                longitude=sample.longitude,
                crisis_type=reasoning.get("crisis_type", ["multi-factor humanitarian stress"]),
                signals=reasoning.get("signals", summaries),
                confidence=float(reasoning.get("confidence", score_result["crisis_score"])),
                crisis_score=float(score_result["crisis_score"]),
                alert_level=str(score_result["alert_level"]),
                created_at=datetime.now(timezone.utc).isoformat(),
                source_counts=source_counts,
                indicators=indicators.to_dict(),
                reasoning=reasoning,
            )
            reports.append(report)
            self.baselines[region] = (self.baselines[region] * 0.6) + (len(region_signals) * 0.4)
        return reports

    def run_cycle(self) -> Dict[str, object]:
        signals = self.collect_signals()
        reports = self.analyze_signals(signals)
        alerts = []
        for report in reports:
            self.reports.appendleft(report)
            if report.alert_level in {"High Alert", "Crisis Likely"}:
                dispatched = self.dispatcher.dispatch(report)
                alert_record = {"report": report.to_dict(), "dispatch": dispatched}
                self.alert_log.appendleft(alert_record)
                alerts.append(alert_record)
        return {
            "signals_collected": len(signals),
            "reports_generated": len(reports),
            "alerts_triggered": len(alerts),
            "reports": [report.to_dict() for report in reports],
            "alerts": alerts,
            "source_health": self.source_health,
        }

    def run_demo(self) -> Dict[str, object]:
        signals = clean_signals(build_demo_signals())
        reports = self.analyze_signals(signals)
        alerts = []
        for report in reports:
            self.reports.appendleft(report)
            dispatched = self.dispatcher.dispatch(report)
            alert_record = {"report": report.to_dict(), "dispatch": dispatched}
            self.alert_log.appendleft(alert_record)
            alerts.append(alert_record)
        return {
            "signals_collected": len(signals),
            "reports_generated": len(reports),
            "alerts_triggered": len(alerts),
            "reports": [report.to_dict() for report in reports],
            "alerts": alerts,
            "source_health": self.source_health,
        }

    def dashboard_state(self) -> Dict[str, object]:
        regions = []
        for report in list(self.reports)[:10]:
            regions.append(
                {
                    "region": report.region,
                    "country": report.country,
                    "latitude": report.latitude,
                    "longitude": report.longitude,
                    "score": report.crisis_score,
                    "level": report.alert_level,
                    "types": report.crisis_type,
                    "signals": report.signals,
                }
            )
        return {
            "reports": [report.to_dict() for report in list(self.reports)],
            "alerts": list(self.alert_log),
            "regions": regions,
            "source_health": self.source_health,
            "mode": "demo" if self.config.demo_mode else "live",
        }

    def start_monitoring(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        def loop() -> None:
            while not self._stop_event.is_set():
                self.run_cycle()
                self._stop_event.wait(self.config.monitor_interval_seconds)

        self._thread = Thread(target=loop, daemon=True)
        self._thread.start()

    def stop_monitoring(self) -> None:
        self._stop_event.set()
