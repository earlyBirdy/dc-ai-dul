"""SNMP connector skeleton.

In a real deployment you would:
  - use pysnmp or equivalent
  - implement OID mappings for PSU, fans, SSD, etc.
  - map values into TelemetryInput.

Here we only provide a simple interface placeholder.
"""

from datetime import datetime
from typing import List

try:
    import pysnmp  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pysnmp = None  # placeholder

from ai_dc_dul.api.schemas import TelemetryInput

class SNMPConnector:
    def __init__(self, host: str, community: str = "public"):
        self.host = host
        self.community = community

    def collect_basic_psu(self) -> List[TelemetryInput]:
        """Placeholder implementation.

        In real code:
          - perform SNMP GET/GETNEXT
          - decode OIDs for PSU temp/power
        """
        now = datetime.utcnow()
        # Demo static data
        return [
            TelemetryInput(
                ts=now,
                asset_id=self.host,
                component_id="PSU1",
                component_type="psu",
                metrics={"temp_c": 45.0, "psu_input_power_w": 320.0},
            )
        ]
