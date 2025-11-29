# dc-ai-dul v1.0  
**AI/ML for Data Center Hardware Health & Depreciation Useful Life (DUL)**   
Supports **OCP (Open Compute)** telemetry + **generic components**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()
[![Status](https://img.shields.io/badge/Status-v0.5-blue.svg)]()
[![OCP Ready](https://img.shields.io/badge/OCP-Telemetry-green.svg)]()

---

## 🚀 Overview

`dc-ai-dul` is an open-source framework to:

- Ingest **OCP Redfish/OpenBMC** telemetry  
- Ingest generic CSV/SNMP/SMART telemetry  
- Normalize into a **unified component schema**  
- Build **degradation features** (ECC slope, PSU ripple, SSD wear, NIC errors...)  
- Train AI/ML models for:
  - **Anomaly detection**
  - **Depreciation Useful Life (DUL) estimation**
  - **Component health score (0–100)**

v0.3 adds:

- A basic **LSTM sequence model** for time-series DUL
- A **CoxPH survival model** for failure risk over time
- Initial **GPU telemetry fields** in the schema and feature builder

---

## 📦 Installation

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🧪 Running the Pipeline

### Generic CSV

```bash
python -m ai_dc_dul.cli.run_pipeline \
  --mode generic \
  --input data/sample/generic_sample.csv
```

### OCP Redfish (live hardware)

```bash
python -m ai_dc_dul.cli.run_pipeline \
  --mode ocp \
  --host 10.0.0.21 --user root --pwd pass123
```

You can also choose which DUL model to run (gradient boosting vs LSTM):

```bash
python -m ai_dc_dul.cli.run_pipeline \
  --mode generic \
  --input data/sample/generic_sample.csv \
  --dul-model gbr        # or lstm
```

---

## 🗺 Roadmap

- v0.4 – FastAPI REST API, dashboards, DCIM connectors  
- v0.5 – Multi-tenant service + authentication  

---

## 📝 License  

MIT – see [LICENSE](LICENSE).


v0.5 adds DCIM/BMS-style connectors (Prometheus, SNMP, Modbus-style stub) feeding the FastAPI service.


v1.0 adds:
- Full fleet planner
- DB schema for assets/components/predictions
- Replacement forecasting
