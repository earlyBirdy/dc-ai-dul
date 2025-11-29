from typing import List

from ai_dc_dul.telemetry_schema import TelemetryRecord
from ai_dc_dul.features.feature_builder import (
    records_to_dataframe,
    make_ml_features,
    build_sequences_for_lstm,
)
from ai_dc_dul.models.anomaly_model import AnomalyModel
from ai_dc_dul.models.dul_model import DULModel
from ai_dc_dul.models.sequence_dul_model import SequenceDULModel
from ai_dc_dul.api.schemas import TelemetryInput

def telemetry_inputs_to_records(inputs: List[TelemetryInput]) -> List[TelemetryRecord]:
    records = []
    for t in inputs:
        records.append(
            TelemetryRecord(
                ts=t.ts,
                asset_id=t.asset_id,
                component_id=t.component_id,
                component_type=t.component_type,  # type: ignore
                vendor=t.vendor,
                model=t.model,
                metrics=t.metrics,
            )
        )
    return records

def run_dul_inference(inputs: List[TelemetryInput], dul_model: str):
    records = telemetry_inputs_to_records(inputs)
    df = records_to_dataframe(records)
    X, _ = make_ml_features(df, label_col="target_dul_days")

    # In a real deployment, load pre-trained models; for v0.4 we train on the fly as a demo.
    ano = AnomalyModel()
    ano.fit(X)
    anomaly_scores = ano.anomaly_score(X)

    if dul_model == "gbr":
        y_dummy = [365.0] * len(X)
        model = DULModel()
        model.fit(X, y_dummy)
        preds = model.predict(X)
    else:
        X_seq, y_seq = build_sequences_for_lstm(df, label_col="target_dul_days")
        if X_seq is None or len(X_seq) == 0:
            raise ValueError("Not enough sequential data for LSTM DUL model.")
        import numpy as np
        if y_seq is None:
            y_seq = np.array([365.0] * len(X_seq), dtype="float32")
        model = SequenceDULModel(n_features=X_seq.shape[-1])
        model.fit(X_seq, y_seq, epochs=3)
        seq_preds = model.predict(X_seq)
        # Simple alignment: extend seq preds to length of X
        preds = list(seq_preds) + [float(seq_preds[-1])] * max(0, len(X) - len(seq_preds))

    results = []
    for i, row in df.iterrows():
        results.append(
            {
                "asset_id": row["asset_id"],
                "component_id": row["component_id"],
                "component_type": row["component_type"],
                "dul_pred_days": float(preds[i]),
                "anomaly_score": float(anomaly_scores[i]),
            }
        )
    return results
