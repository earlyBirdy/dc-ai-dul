import requests
from typing import List
from datetime import datetime

from ai_dc_dul.telemetry_schema import TelemetryRecord, normalize_ocp_metric_name

class OCPRedfishIngestor:
    """Redfish-based ingestor for OCP/OpenBMC systems (simplified v0.3)."""

    def __init__(self, host: str, user: str, pwd: str, verify_ssl: bool = False):
        self.base = f"https://{host}/redfish/v1"
        self.auth = (user, pwd)
        self.verify_ssl = verify_ssl

    def _get(self, path: str):
        url = self.base + path
        resp = requests.get(url, auth=self.auth, verify=self.verify_ssl, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def ingest(self, chassis_id: str = "1", system_id: str = "1") -> List[TelemetryRecord]:
        ts = datetime.utcnow()
        records: List[TelemetryRecord] = []

        # 1) Power / PSU
        try:
            power = self._get(f"/Chassis/{chassis_id}/Power")
            for psu in power.get("PowerSupplies", []):
                metrics = {}
                for k, v in psu.items():
                    if isinstance(v, (int, float)):
                        metrics[normalize_ocp_metric_name(k)] = v
                rec = TelemetryRecord(
                    ts=ts,
                    asset_id=system_id,
                    component_id=psu.get("MemberId", "PSU"),
                    component_type="psu",
                    metrics=metrics,
                    meta={"source": "redfish_power"},
                )
                records.append(rec)
        except Exception:
            pass

        # 2) Thermal / fans
        try:
            thermal = self._get(f"/Chassis/{chassis_id}/Thermal")
            for fan in thermal.get("Fans", []):
                metrics = {}
                reading = fan.get("Reading")
                if isinstance(reading, (int, float)):
                    metrics["fan_rpm"] = float(reading)
                rec = TelemetryRecord(
                    ts=ts,
                    asset_id=system_id,
                    component_id=fan.get("MemberId", "FAN"),
                    component_type="fan",
                    metrics=metrics,
                    meta={"source": "redfish_thermal"},
                )
                records.append(rec)
        except Exception:
            pass

        # 3) Network / NIC 3.0 (simplified)
        try:
            adapters = self._get(f"/Systems/{system_id}/NetworkAdapters")
            for m in adapters.get("Members", []):
                nic = self._get(m["@odata.id"][len(self.base):])
                metrics = {}
                for k, v in nic.items():
                    if isinstance(v, (int, float)):
                        metrics[normalize_ocp_metric_name(k)] = v
                rec = TelemetryRecord(
                    ts=ts,
                    asset_id=system_id,
                    component_id=nic.get("Id", "NIC"),
                    component_type="nic",
                    metrics=metrics,
                    meta={"source": "redfish_nic"},
                )
                records.append(rec)
        except Exception:
            pass

        # 4) Storage / SSD (simplified)
        try:
            storage = self._get(f"/Systems/{system_id}/Storage")
            for ctrl in storage.get("Members", []):
                controller = self._get(ctrl["@odata.id"][len(self.base):])
                for dref in controller.get("Drives", []):
                    d = self._get(dref["@odata.id"][len(self.base):])
                    metrics = {}
                    for k, v in d.items():
                        if isinstance(v, (int, float)):
                            metrics[normalize_ocp_metric_name(k)] = v
                    rec = TelemetryRecord(
                        ts=ts,
                        asset_id=system_id,
                        component_id=d.get("Id", "SSD"),
                        component_type="ssd",
                        metrics=metrics,
                        meta={"source": "redfish_ssd"},
                    )
                    records.append(rec)
        except Exception:
            pass

        return records
