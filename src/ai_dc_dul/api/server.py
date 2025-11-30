from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from pathlib import Path
import logging

from ai_dc_dul import __version__

logger = logging.getLogger(__name__)

app = FastAPI(title="dc-ai-dul API", version=__version__)

# Allow local dev frontend (Vite) and same-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve absolute path to repo root and frontend/dist
THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[3]  # .../dc-ai-dul
FRONTEND_DIST = REPO_ROOT / "frontend" / "dist"

if FRONTEND_DIST.is_dir():
    logger.info(f"Mounting frontend from {FRONTEND_DIST}")
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")
else:
    logger.warning(
        f"frontend/dist not found at {FRONTEND_DIST}, /app will return 404. "
        "Run `cd frontend && npm run build` or ./run_all.sh to build the UI."
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "dc-ai-dul", "version": __version__}


@app.get("/")
def root():
    return {
        "message": "dc-ai-dul API is running. Open /app for the dashboard, or /docs for the API docs.",
        "dashboard": "/app",
        "docs": "/docs",
    }


# --- Demo DCIM-style dashboard APIs ---
@app.get("/api/fleet/summary")
def fleet_summary():
    """High-level fleet stats for Overview page."""
    return {
        "generated_at": datetime.utcnow().isoformat(),
        "total_assets": 16,
        "total_components": 224,
        "avg_dul_days": 196.4,
        "risk_breakdown": {
            "red": 8,
            "orange": 34,
            "green": 182,
        },
    }


@app.get("/api/fleet/dul_trend")
def dul_trend():
    """Simple DUL trend data for chart in Overview."""
    base = datetime.utcnow()
    dates = []
    values = []
    for i in range(14, -1, -1):
        dt = base - timedelta(days=i)
        dates.append(dt.strftime("%Y-%m-%d"))
        values.append(150 + i * 3)
    return {"dates": dates, "avg_dul_days": values}


@app.get("/api/fleet/heatmap")
def fleet_heatmap():
    """Rack-level risk heatmap for Fleet tab."""
    return {
        "racks": ["R01", "R02", "R03", "R04", "R05"],
        "rows": [
            {"rack": "R01", "low": 3, "medium": 5, "high": 2},
            {"rack": "R02", "low": 1, "medium": 7, "high": 4},
            {"rack": "R03", "low": 0, "medium": 3, "high": 8},
            {"rack": "R04", "low": 5, "medium": 2, "high": 1},
            {"rack": "R05", "low": 2, "medium": 6, "high": 3},
        ],
    }


@app.get("/api/fleet/replacements")
def fleet_replacements():
    """Upcoming replacements list for Fleet tab table."""
    base = datetime.utcnow().date()
    items = []
    for i, name in enumerate(["PSU1", "SSD0", "GPU0", "FAN3", "SSD1", "PSU2"], start=1):
        items.append(
            {
                "asset_id": f"server-{i:02d}",
                "component_id": name,
                "component_type": "psu" if "PSU" in name else "ssd" if "SSD" in name else "gpu" if "GPU" in name else "fan",
                "risk_level": "red" if i <= 2 else "orange" if i <= 4 else "green",
                "predicted_dul_days": 30 * i,
                "replacement_date": str(base + timedelta(days=30 * i)),
                "capex_estimate": 250.0 * i,
            }
        )
    return {"items": items}


@app.get("/api/docs/summary")
def docs_summary():
    return {
        "sections": [
            {
                "title": "Sensors",
                "body": "PSU, SSD/NVMe, GPU, Fans, Node (CPU/VRM), and Rack Env telemetry are used because they correlate strongly with hardware degradation and MTBF decay.",
            },
            {
                "title": "Feature Engineering",
                "body": "We derive slopes, accelerations, efficiency drift, thermal cycles, and stress indices from raw sensor metrics for stable ML inputs. See docs/FEATURE_ENGINEERING.md for details.",
            },
            {
                "title": "Models",
                "body": "We use Gradient Boosted Regression, LSTM sequences, and Cox Proportional Hazards for different layers of DUL/RUL prediction. See docs/DUL_MODEL_THEORY.md.",
            },
            {
                "title": "Deployment",
                "body": "dc-ai-dul can run locally, in Docker, or in Kubernetes, with offline model packs supported for air-gapped DCs. See docs/DEPLOYMENT_GUIDE.md.",
            },
        ]
    }
