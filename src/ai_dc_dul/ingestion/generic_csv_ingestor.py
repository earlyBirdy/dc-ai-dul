import pandas as pd
from datetime import datetime
from typing import List

from ai_dc_dul.telemetry_schema import TelemetryRecord, ComponentType

def load_generic_csv(path: str) -> List[TelemetryRecord]:
    """Simple CSV ingestor for generic hardware.

    Required columns:
      ts, asset_id, component_id, component_type
    Optional columns:
      vendor, model, target_dul_days, failed, plus any metric columns.
    """
    df = pd.read_csv(path)
    required = ["ts", "asset_id", "component_id", "component_type"]
    for c in required:
        if c not in df.columns:
            raise ValueError(f"Missing required column: {c}")

    records: List[TelemetryRecord] = []
    for _, row in df.iterrows():
        ts = datetime.fromisoformat(str(row["ts"]))
        comp_type: ComponentType = row["component_type"]  # type: ignore

        metrics = {}
        for col in df.columns:
            if col in required + ["vendor", "model", "target_dul_days", "failed"]:
                continue
            val = row[col]
            if pd.isna(val):
                continue
            try:
                v = float(val)
            except Exception:
                continue
            metrics[col] = v

        record = TelemetryRecord(
            ts=ts,
            asset_id=str(row["asset_id"]),
            component_id=str(row["component_id"]),
            component_type=comp_type,
            vendor=str(row["vendor"]) if "vendor" in df.columns else None,
            model=str(row["model"]) if "model" in df.columns else None,
            metrics=metrics,
            target_dul_days=float(row["target_dul_days"])
            if "target_dul_days" in df.columns and not pd.isna(row["target_dul_days"])
            else None,
            failed=int(row["failed"])
            if "failed" in df.columns and not pd.isna(row["failed"])
            else None,
            meta={},
        )
        records.append(record)

    return records
