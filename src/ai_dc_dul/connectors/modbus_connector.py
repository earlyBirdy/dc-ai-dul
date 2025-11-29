"""Modbus-style connector skeleton.

Intended for:
  - BMS / electrical rooms
  - CRAC/CHW units
  - Rack PDUs that expose Modbus registers.

In real deployments you would:
  - use pymodbus
  - map register addresses to metrics
  - convert per-rack data into rack_env TelemetryInput.
"""

from datetime import datetime
from typing import List

try:
    import pymodbus  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pymodbus = None

from ai_dc_dul.api.schemas import TelemetryInput

class ModbusConnector:
    def __init__(self, host: str, port: int = 502):
        self.host = host
        self.port = port

    def collect_rack_env(self, rack_id: str = "rack-01") -> List[TelemetryInput]:
        """Placeholder implementation that mimics rack environment telemetry."""
        now = datetime.utcnow()
        return [
            TelemetryInput(
                ts=now,
                asset_id=rack_id,
                component_id="RACK_ENV",
                component_type="rack_env",
                metrics={
                    "temp_c": 27.5,
                    "humidity_pct": 45.0,
                },
            )
        ]
