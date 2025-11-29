from typing import List, Dict, Any, Tuple
import pandas as pd

from ai_dc_dul.telemetry_schema import TelemetryRecord

def records_to_dataframe(records: List[TelemetryRecord]) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for r in records:
        base = {
            "ts": r.ts,
            "asset_id": r.asset_id,
            "component_id": r.component_id,
            "component_type": r.component_type,
            "vendor": r.vendor,
            "model": r.model,
            "target_dul_days": r.target_dul_days,
            "failed": r.failed,
        }
        if r.metrics:
            base.update(r.metrics)
        rows.append(base)
    return pd.DataFrame(rows)

def make_ml_features(
    df: pd.DataFrame,
    label_col: str = "target_dul_days",
) -> Tuple[pd.DataFrame, pd.Series]:
    if "ts" in df.columns:
        df = df.copy()
        df["ts_epoch"] = pd.to_datetime(df["ts"]).astype("int64") // 10**9

    id_cols = ["ts", "asset_id", "component_id", "vendor", "model"]
    feature_cols = []
    for col in df.columns:
        if col in id_cols:
            continue
        if col == label_col:
            continue
        if df[col].dtype.kind in "biufc":
            feature_cols.append(col)

    X = df[feature_cols].fillna(0.0)
    y = df[label_col] if label_col in df.columns else None
    return X, y

def build_sequences_for_lstm(
    df: pd.DataFrame,
    seq_len: int = 16,
    label_col: str = "target_dul_days",
):
    """Build per-component time-series sequences for LSTM."""
    df = df.copy()
    df["ts"] = pd.to_datetime(df["ts"])
    df.sort_values(["asset_id", "component_id", "ts"], inplace=True)

    id_cols = ["ts", "asset_id", "component_id", "vendor", "model"]
    feature_cols = []
    for col in df.columns:
        if col in id_cols:
            continue
        if col == label_col:
            continue
        if df[col].dtype.kind in "biufc":
            feature_cols.append(col)

    X_list = []
    y_list = []

    import numpy as np

    for (asset, comp), g in df.groupby(["asset_id", "component_id"]):
        g = g.reset_index(drop=True)
        if len(g) < seq_len:
            continue
        for start in range(0, len(g) - seq_len + 1):
            window = g.iloc[start : start + seq_len]
            X_list.append(window[feature_cols].values)
            if label_col in g.columns:
                y_list.append(float(window[label_col].iloc[-1]))

    X_seq = np.array(X_list, dtype="float32")
    y_seq = np.array(y_list, dtype="float32") if y_list else None
    return X_seq, y_seq
