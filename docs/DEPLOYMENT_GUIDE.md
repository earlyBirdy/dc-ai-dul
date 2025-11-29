
# DEPLOYMENT_GUIDE.md — Deploying dc-ai-dul in Production

## 1. Overview
This guide explains how to deploy dc-ai-dul in:
- Local development
- Docker Compose
- Kubernetes (K8s)
- Air‑gapped / offline environments

---

## 2. Requirements
- Python 3.10+
- Postgres/TimescaleDB
- Optional: Prometheus, Grafana
- Optional: GPU node for LSTM acceleration

---

## 3. Local Deployment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
uvicorn ai_dc_dul.api.server:app --reload
```

Access:
- API: http://localhost:8000/api
- Dashboard: http://localhost:8000/dashboard

---

## 4. Docker Compose Deployment

```
docker compose up -d
```

Services:
- api  
- postgres  
- grafana  
- ingestion worker (future)

---

## 5. Kubernetes Deployment (v1.3+)

Components:
- Deployment (FastAPI)
- Service (ClusterIP)
- Ingress
- ConfigMap (model settings)
- Secret (DB credentials)
- CronJob (daily aggregation)

---

## 6. Offline/Air‑Gapped Deployment

Supported:
- Model stored in `/models/`
- No external telemetry required
- CLI pipeline:

```
python -m ai_dc_dul.cli.run_pipeline --offline --model-dir models/
```

---

## 7. Monitoring & Alerting

Grafana dashboards included:
- Fleet health view  
- Component risk heatmap  
- Replacement forecast board  

Prometheus metrics exposed at:
```
/metrics
```

