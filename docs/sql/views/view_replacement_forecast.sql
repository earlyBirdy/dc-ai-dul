CREATE OR REPLACE VIEW replacement_forecast AS
SELECT
    asset_id,
    component_id,
    dul_pred_days,
    NOW() + (dul_pred_days || ' days')::interval AS replacement_date,
    CASE
        WHEN dul_pred_days < 30 THEN 'red'
        WHEN dul_pred_days < 90 THEN 'orange'
        ELSE 'green'
    END AS risk
FROM latest_dul_per_component;
