
# ML_PIPELINE.md — Data → Features → Models → DUL Output

## 1. Overview
This document explains the full machine‑learning pipeline used in dc-ai-dul to transform raw telemetry into DUL/RUL predictions.

## 2. Pipeline Stages

### Stage 1 — Telemetry Ingestion
Sources:
- Redfish / OCP Telemetry
- SNMP / Prometheus
- IPMI/BMC
- smartctl (SSD)
- nvidia‑smi (GPU)
- Modbus/BMS (Rack environment)

Output: `TelemetryInput` objects.

---

### Stage 2 — Feature Engineering
Raw → engineered features:
- Temperature slopes
- Wear-rate acceleration
- ECC error acceleration
- Efficiency drift
- Thermal cycles
- EM stress index (GPU)
- Cooling degradation index (fan + rack temp)

These features significantly reduce noise and improve model stability.

---

### Stage 3 — Model Selection
dc-ai-dul uses three ML model families:

1. **Gradient Boosting Regressor (GBR)**  
   - Handles nonlinear interactions well  
   - Low latency  
   - Great for per-component predictions  

2. **LSTM Sequence Model**  
   - Learns long-term temporal degradation patterns  
   - Useful for GPU/SSD telemetry traces  

3. **Cox Proportional Hazards (CoxPH)**  
   - Survival analysis for fleet‑level failure curves  
   - Predicts hazard ratios and risk functions  

---

### Stage 4 — DUL Prediction
The model outputs:
- DUL (Depreciation Useful Life score)
- RUL (days/months remaining)
- Failure-risk probability
- Component-level health score
- Fleet‑level aggregated risk

---

### Stage 5 — Storage & API Output
Results stored in:
- Postgres/Timescale
- S3 snapshots (future)

Accessible via:
```
GET /api/dul/component/<id>
GET /api/dul/fleet
GET /api/dul/predict
```

