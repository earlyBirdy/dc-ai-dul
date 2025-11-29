"""Prometheus connector: pull metrics and convert to TelemetryInput list.

This is a simple example that:
  - queries Prometheus HTTP API
  - maps results to TelemetryInput
  - can be used to feed /api/predict.

In real deployments, you would:
  - parameterize Prometheus URL and queries
  - handle auth/TLS
  - support many metric families.
"""

from datetime import datetime
from typing import List

import requests

from ai_dc_dul.api.schemas import TelemetryInput

class PrometheusConnector:
    def __init__(self, base_url: str = "http://localhost:9090"):
        self.base_url = base_url.rstrip("/")

    def _query(self, expr: str):
        resp = requests.get(
            f"{self.base_url}/api/v1/query",
            params={"query": expr},
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()["data"]["result"]

    def collect_psu_temp(self, expr: str = "node_psu_temp_c") -> List[TelemetryInput]:
        """Example: map PSU temp metrics into TelemetryInput objects."""
        results = self._query(expr)
        now = datetime.utcnow()
        telemetry: List[TelemetryInput] = []
        for item in results:
            labels = item.get("metric", {})
            value = float(item["value"][1])
            asset = labels.get("instance", "server-unknown")
            comp = labels.get("psu", "PSU1")
            telemetry.append(
                TelemetryInput(
                    ts=now,
                    asset_id=asset,
                    component_id=comp,
                    component_type="psu",
                    metrics={"temp_c": value},
                )
            )
        return telemetry
