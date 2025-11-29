import argparse

from ai_dc_dul.ingestion.generic_csv_ingestor import load_generic_csv
from ai_dc_dul.ingestion.ocp_redfish_ingestor import OCPRedfishIngestor
from ai_dc_dul.features.feature_builder import (
    records_to_dataframe,
    make_ml_features,
    build_sequences_for_lstm,
)
from ai_dc_dul.models.anomaly_model import AnomalyModel
from ai_dc_dul.models.dul_model import DULModel
from ai_dc_dul.models.sequence_dul_model import SequenceDULModel

def main():
    parser = argparse.ArgumentParser(description="Run dc-ai-dul v0.3 pipeline.")
    parser.add_argument("--mode", choices=["generic", "ocp"], default="generic")
    parser.add_argument("--input", help="Path to CSV (for generic mode).")
    parser.add_argument("--host", help="Redfish host (for ocp mode).")
    parser.add_argument("--user", help="Redfish username.")
    parser.add_argument("--pwd", help="Redfish password.")
    parser.add_argument(
        "--dul-model",
        choices=["gbr", "lstm"],
        default="gbr",
        help="DUL model type: gradient boosting (gbr) or LSTM (lstm).",
    )
    args = parser.parse_args()

    if args.mode == "generic":
        if not args.input:
            parser.error("--input is required for generic mode")
        records = load_generic_csv(args.input)
    else:
        if not (args.host and args.user and args.pwd):
            parser.error("--host, --user, --pwd are required for ocp mode")
        ing = OCPRedfishIngestor(args.host, args.user, args.pwd)
        records = ing.ingest()

    df = records_to_dataframe(records)
    X, y = make_ml_features(df)

    print(f"Loaded {len(df)} records, {X.shape[1]} feature columns.")
    if y is None:
        print("No target_dul_days label found; DUL model will not be trained.")
        return

    # Anomaly model
    ano = AnomalyModel()
    ano.fit(X)
    scores = ano.anomaly_score(X)

    if args.dul_model == "gbr":
        dul = DULModel()
        mae = dul.fit(X, y)
        y_pred = dul.predict(X)
        print(f"Gradient boosting DUL model MAE (train): {mae:.2f} days")
    else:
        X_seq, y_seq = build_sequences_for_lstm(df)
        if X_seq is None or len(X_seq) == 0 or y_seq is None:
            print("Not enough sequential data for LSTM; aborting LSTM training.")
            return
        n_features = X_seq.shape[-1]
        seq_model = SequenceDULModel(n_features=n_features)
        loss = seq_model.fit(X_seq, y_seq, epochs=5)
        y_pred = seq_model.predict(X_seq)
        print(f"LSTM DUL model training loss: {loss:.4f}")
        scores = scores[: len(y_pred)]

    df_out = df.copy()
    df_out["anomaly_score"] = scores
    df_out["dul_pred_days"] = y_pred

    cols = [
        "asset_id",
        "component_id",
        "component_type",
        "target_dul_days",
        "dul_pred_days",
        "anomaly_score",
    ]
    print("\nSample predictions:")
    print(df_out[cols].head(10).to_string(index=False))

if __name__ == "__main__":
    main()
