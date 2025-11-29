# Architecture

High-level pipeline:

1. Ingestion
   - `OCPRedfishIngestor` for OCP/OpenBMC/Redfish endpoints
   - `load_generic_csv` for CSV-based telemetry

2. Schema
   - `TelemetryRecord` is the unified representation of one component at one time

3. Feature Extraction
   - `records_to_dataframe` flattens telemetry to a pandas DataFrame
   - `make_ml_features` builds tabular features for tree models
   - `build_sequences_for_lstm` builds per-component time-series tensors

4. Models
   - `AnomalyModel` (IsolationForest)
   - `DULModel` (GradientBoostingRegressor)
   - `SequenceDULModel` (PyTorch LSTM)
   - `SurvivalDULModel` (CoxPH via lifelines)

5. CLI
   - `run_pipeline.py` orchestrates ingestion → features → models → predictions
