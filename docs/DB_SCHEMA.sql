CREATE TABLE assets (
    asset_id TEXT PRIMARY KEY,
    name TEXT,
    location TEXT,
    rack TEXT,
    vendor TEXT,
    model TEXT,
    deployed_at TIMESTAMP,
    metadata JSONB
);

CREATE TABLE components (
    component_id TEXT,
    asset_id TEXT REFERENCES assets(asset_id),
    component_type TEXT,
    vendor TEXT,
    model TEXT,
    serial_number TEXT,
    installed_at TIMESTAMP,
    metadata JSONB,
    PRIMARY KEY (asset_id, component_id)
);

CREATE TABLE telemetry_raw (
    ts TIMESTAMPTZ NOT NULL,
    asset_id TEXT,
    component_id TEXT,
    metrics JSONB,
    PRIMARY KEY (ts, asset_id, component_id)
);

CREATE TABLE dul_predictions (
    ts TIMESTAMPTZ NOT NULL,
    asset_id TEXT,
    component_id TEXT,
    dul_pred_days DOUBLE PRECISION,
    anomaly_score DOUBLE PRECISION,
    model_version TEXT,
    PRIMARY KEY (ts, asset_id, component_id)
);

CREATE TABLE failures (
    asset_id TEXT,
    component_id TEXT,
    failed_at TIMESTAMPTZ,
    failure_type TEXT,
    metadata JSONB
);

CREATE TABLE planner_output (
    generated_at TIMESTAMPTZ,
    asset_id TEXT,
    component_id TEXT,
    replacement_date DATE,
    predicted_dul DOUBLE PRECISION,
    risk_level TEXT,
    capex_estimate DOUBLE PRECISION
);
