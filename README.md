# dc-ai-dul — Data-Center Depreciation Useful Life (DUL) Prediction

AI/ML models for predicting hardware lifespan, failure risk, and component aging across servers, racks, GPUs, SSDs, PSUs, and data‑center infrastructure.

[![license](https://img.shields.io/badge/license-Apache%202.0-blue.svg)]()
[![python](https://img.shields.io/badge/python-3.10+-yellow.svg)]()
[![status](https://img.shields.io/badge/status-active-success.svg)]()
[![docs](https://img.shields.io/badge/docs-available-brightgreen.svg)]()
[![model](https://img.shields.io/badge/model-GBR%20%7C%20LSTM%20%7C%20CoxPH-purple.svg)]()

---

## 🔥 What is DUL?

DUL (Depreciation Useful Life) = ML-estimated remaining lifespan of a data‑center component, using telemetry signals:

- PSU temperature & efficiency drift  
- SSD wear / SMART indicators  
- GPU temperature, utilization, power  
- Fan RPM instability  
- CPU/VRM temperature, ECC error acceleration  
- Rack temperature, humidity, airflow  

Fully vendor‑neutral, OCP‑aligned, and supports Redfish Telemetry Service.

---

# 📘 Documentation Index

### **Sensor & ML Foundations**
- `docs/SENSORS.md`
- `docs/FEATURE_ENGINEERING.md`
- `docs/CONNECTOR_SPEC.md`

### **ML Pipeline & Theory**
- `docs/ML_PIPELINE.md`
- `docs/DUL_MODEL_THEORY.md`

### **Deployment**
- `docs/DEPLOYMENT_GUIDE.md`
- Architecture diagrams in: `docs/ARCHITECTURE_DIAGRAMS/`

---

# 🏗 Architecture Overview

```
Sensors → Connectors → Feature Engineering → ML Models → DUL/RUL Output → API & Dashboard
```

**Models used:**  
- Gradient Boosted Regression (GBR)  
- LSTM (temporal degradation)  
- Cox Proportional Hazards (fleet hazard models)

---

# 🚀 Installation

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Verify:

```
python -c "import ai_dc_dul; print(ai_dc_dul.__version__)"
```

---

# ▶️ Run the Pipeline

### Standard example:

```
python -m ai_dc_dul.cli.run_pipeline   --mode generic   --input data/sample/generic_sample.csv   --dul-model gbr
```

### Offline mode:

```
python -m ai_dc_dul.cli.run_pipeline --offline --model-dir models/
```

---

# 🌐 FastAPI Dashboard

```
uvicorn ai_dc_dul.api.server:app --reload
```

- Dashboard → http://localhost:8000/dashboard  
- API docs → http://localhost:8000/docs  
- Health → http://localhost:8000/health  

---

# 📊 Grafana Dashboards

Import JSON dashboards from `docs/grafana/`.

Dashboards included:  
- Fleet Overview  
- Component Health  
- Replacement Forecast  

---

# 🛣 Roadmap

### v1.3  
- SSD/GPU/Fan/Node connectors  
- Offline model loader  
- Hazard engine (CoxPH)  
- Daily aggregation

### v1.4  
- Full temporal degradation dataset  
- GPU farm LSTM inference  
- Replacement planning

### v2.0  
- Vibration / acoustic sensors  
- Liquid cooling telemetry  
- Multi‑rack simulation  
- Edge deployment  

---

# 🤝 Contributing

See connector rules in:  

```
docs/CONNECTOR_SPEC.md
```

---

# 📜 License

Apache 2.0  
© dc-ai-dul
