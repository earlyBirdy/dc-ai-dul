# dc-ai-dul — Data-Center Depreciation Useful Life (DUL) Prediction

AI/ML for predicting hardware lifespan, failure risk, and component aging across servers, racks, GPUs, SSDs, PSUs, and data‑center infrastructure.

[![license](https://img.shields.io/badge/license-Apache%202.0-blue.svg)]()
[![python](https://img.shields.io/badge/python-3.10+-yellow.svg)]()
[![status](https://img.shields.io/badge/status-active-success.svg)]()
[![docs](https://img.shields.io/badge/docs-available-brightgreen.svg)]()
[![model](https://img.shields.io/badge/model-GBR%20%7C%20LSTM%20%7C%20CoxPH-purple.svg)]()

---

## 🔥 What is DUL?

**DUL (Depreciation Useful Life)** = ML‑estimated remaining lifespan of a data‑center component, based on telemetry such as:

- PSU temperature & efficiency drift  
- SSD wear / SMART indicators  
- GPU temperature, utilization, power  
- Fan RPM instability  
- CPU/VRM temperature, ECC error acceleration  
- Rack temperature, humidity, airflow  

The project is vendor‑neutral, OCP‑aligned, and supports Redfish Telemetry Service.

---

# 🚀 One‑Command Start

After cloning the repo and dropping the patched files:

```bash
cd dc-ai-dul
chmod +x run_all.sh
./run_all.sh
```

This will:

1. Create/activate a Python virtualenv (`.venv`)  
2. Install Python dependencies (`requirements.txt`, `pip install -e .`)  
3. Build the React/Vite frontend in `frontend/`  
4. Start the FastAPI backend + static dashboard at **http://localhost:8000/app**

---

# 🌐 Web Dashboard

Once `./run_all.sh` is running, open:

- **Dashboard (SPA):** http://localhost:8000/app  
- **API docs (Swagger):** http://localhost:8000/docs  
- **Health:** http://localhost:8000/health  

The single‑page app has a left sidebar with:

- **Overview** — fleet summary + DUL trend chart  
- **Fleet** — rack risk “heatmap” + upcoming replacements table  
- **Docs** — high‑level summary of sensors, feature engineering, models, deployment  
- **Settings** — placeholder for configuring thresholds, model type, etc.

---

# 📘 Documentation Index

All detailed docs live under `docs/`:

### Sensor & ML Foundations

- `docs/SENSORS.md` — six high‑impact sensor categories  
- `docs/FEATURE_ENGINEERING.md` — how raw metrics become ML features  
- `docs/CONNECTOR_SPEC.md` — Prometheus, SNMP, IPMI, Redfish, nvidia‑smi, smartctl ingestion

### ML Pipeline & Theory

- `docs/ML_PIPELINE.md` — Data → Features → Models → DUL/RUL  
- `docs/DUL_MODEL_THEORY.md` — GBR, CoxPH, LSTM modeling theory

### Deployment

- `docs/DEPLOYMENT_GUIDE.md` — local, Docker, Kubernetes, offline  
- `docs/ARCHITECTURE_DIAGRAMS/diagram.svg` — high‑level architecture

---

# 🏗 Architecture Overview

```text
Sensors → Connectors → Feature Engineering → ML Models → DUL/RUL → API & Dashboard
```

**Sensor categories:**

- PSU  
- SSD / NVMe  
- GPU  
- Fans  
- Node (CPU / VRM / memory)  
- Rack environment  

**Model families:**

- Gradient Boosted Regressor (GBR) — per‑component DUL  
- LSTM sequence models — temporal degradation  
- Cox Proportional Hazards (CoxPH) — fleet‑level survival analysis  

---

# ⚙️ Manual Setup (if not using run_all.sh)

### 1. Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 2. Frontend (Vite + React)

```bash
cd frontend
npm install
npm run build   # outputs to frontend/dist with base=/app/
cd ..
```

### 3. Start backend

```bash
uvicorn ai_dc_dul.api.server:app --reload
```

Then browse to: http://localhost:8000/app

---

# ▶️ Running the DUL Pipeline (CLI)

Example CLI run (independent of the web UI):

```bash
python -m ai_dc_dul.cli.run_pipeline   --mode generic   --input data/sample/generic_sample.csv   --dul-model gbr
```

Offline mode with local models:

```bash
python -m ai_dc_dul.cli.run_pipeline --offline --model-dir models/
```

---

# 🛣 Roadmap (High‑Level)

- **v1.3**
  - Real SSD/GPU/Fan/Node connectors  
  - Offline model pack loader  
  - CoxPH fleet hazard engine  
  - Daily aggregation jobs  

- **v1.4**
  - Full temporal degradation history  
  - GPU cluster LSTM inference  
  - Replacement recommendation engine  

- **v2.0**
  - Vibration / acoustic / liquid cooling sensors  
  - Multi‑rack thermal simulation  
  - Edge deployment (on‑box inference)

---

# 🤝 Contributing

PRs welcome.

For connector guidelines and expected telemetry schema, see:

```text
docs/CONNECTOR_SPEC.md
```

---

# 📜 License

Apache 2.0  
© dc‑ai‑dul
