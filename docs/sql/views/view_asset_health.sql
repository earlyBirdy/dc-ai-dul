CREATE OR REPLACE VIEW asset_health AS
SELECT
    asset_id,
    AVG(dul_pred_days) AS avg_dul,
    MIN(dul_pred_days) AS min_dul,
    MAX(anomaly_score) AS worst_anomaly
FROM latest_dul_per_component
GROUP BY asset_id;
