from __future__ import annotations

from typing import List

from backend.data_sources.base import SourceClient
from backend.models import UnifiedSignal


class OpenWeatherClient(SourceClient):
    source_name = "openweather"
    category = "environmental"
    endpoint = "https://api.openweathermap.org/data/2.5/weather"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode or not self.config.openweather_key:
            region = self.config.tracked_regions[0]
            return [
                self.region_signal(
                    region,
                    title="Severe heat and rainfall deficit",
                    text="Weather anomaly model indicates persistent heat and low rainfall in Northern Kenya.",
                    keywords=["drought", "heat", "rainfall deficit"],
                    severity=0.92,
                    metadata={"temperature_c": 38.1, "rainfall_anomaly": 0.84},
                )
            ]

        signals: List[UnifiedSignal] = []
        for region in self.config.tracked_regions:
            data = self.request_json(
                self.endpoint,
                params={
                    "lat": region.latitude,
                    "lon": region.longitude,
                    "appid": self.config.openweather_key,
                    "units": "metric",
                },
            )
            rain = data.get("rain", {}).get("1h", 0.0)
            temp = data.get("main", {}).get("temp", 0.0)
            severity = 0.4 + min(temp / 50.0, 0.3) + (0.2 if rain == 0 else 0.0)
            signals.append(
                self.region_signal(
                    region,
                    title="OpenWeather anomaly",
                    text=f"Observed temperature {temp}C with rain={rain}mm.",
                    keywords=["temperature anomaly", "rainfall anomaly"],
                    severity=severity,
                    metadata={"raw": data},
                )
            )
        return signals


class NASAEarthDataClient(SourceClient):
    source_name = "nasa_earthdata"
    category = "environmental"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode:
            region = self.config.tracked_regions[0]
            return [
                self.region_signal(
                    region,
                    title="Satellite dryness index elevated",
                    text="Earth observation layers show soil moisture deficits and shrinking vegetation cover.",
                    keywords=["soil moisture deficit", "vegetation stress", "drought"],
                    severity=0.88,
                    metadata={"ndvi_delta": -0.31, "soil_moisture_delta": -0.27},
                )
            ]

        data = self.request_json(
            self.config.nasa_earthdata_url,
            params={"keyword": "drought", "page_size": 5},
        )
        region = self.config.tracked_regions[0]
        entries = data.get("feed", {}).get("entry", [])
        return [
            self.region_signal(
                region,
                title=entry.get("title", "EarthData granule"),
                text=entry.get("summary", ""),
                keywords=["satellite anomaly"],
                severity=0.52,
                metadata={"id": entry.get("id")},
            )
            for entry in entries
        ]


class NOAAClimateClient(SourceClient):
    source_name = "noaa_climate"
    category = "environmental"
    endpoint = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode or not self.config.noaa_token:
            region = self.config.tracked_regions[0]
            return [
                self.region_signal(
                    region,
                    title="NOAA climate anomaly proxy",
                    text="Climate baselines indicate significant rainfall departure from normal conditions.",
                    keywords=["rainfall departure", "climate anomaly"],
                    severity=0.79,
                    metadata={"precipitation_percent_normal": 42},
                )
            ]

        region = self.config.tracked_regions[0]
        data = self.request_json(
            self.endpoint,
            headers={"token": self.config.noaa_token},
            params={"datasetid": "GHCND", "limit": 5},
        )
        return [
            self.region_signal(
                region,
                title="NOAA climate datapoint",
                text=f"Observed value: {item.get('value')}",
                keywords=["climate datapoint"],
                severity=0.5,
                metadata={"raw": item},
            )
            for item in data.get("results", [])
        ]


class GlobalFloodMonitoringClient(SourceClient):
    source_name = "gfms"
    category = "environmental"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode or not self.config.gfms_api_url:
            return []

        data = self.request_json(self.config.gfms_api_url)
        region = self.config.tracked_regions[2]
        return [
            self.region_signal(
                region,
                title="GFMS flood signal",
                text=item.get("summary", "Flood monitoring event"),
                keywords=["flood", "water level"],
                severity=float(item.get("severity", 0.6)),
                metadata={"raw": item},
            )
            for item in data.get("events", [])
        ]


class CopernicusClimateClient(SourceClient):
    source_name = "copernicus"
    category = "environmental"

    def fetch(self) -> List[UnifiedSignal]:
        if self.config.demo_mode or not self.config.copernicus_api_url:
            return []

        data = self.request_json(self.config.copernicus_api_url)
        region = self.config.tracked_regions[0]
        return [
            self.region_signal(
                region,
                title="Copernicus anomaly",
                text=item.get("description", "Climate anomaly"),
                keywords=["climate anomaly"],
                severity=float(item.get("severity", 0.6)),
                metadata={"raw": item},
            )
            for item in data.get("events", [])
        ]
