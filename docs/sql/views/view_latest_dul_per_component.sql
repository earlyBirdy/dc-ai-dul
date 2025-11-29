CREATE OR REPLACE VIEW latest_dul_per_component AS
SELECT DISTINCT ON (asset_id, component_id)
    asset_id,
    component_id,
    dul_pred_days,
    anomaly_score,
    ts
FROM dul_predictions
ORDER BY asset_id, component_id, ts DESC;
