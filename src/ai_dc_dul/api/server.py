from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ai_dc_dul import __version__
from ai_dc_dul.api.schemas import PredictRequest
from ai_dc_dul.api.services import run_dul_inference

app = FastAPI(title="dc-ai-dul API", version=__version__)

templates = Jinja2Templates(directory="templates")

@app.get("/health")
def health():
    return {"status": "ok", "service": "dc-ai-dul", "version": __version__}

@app.post("/api/predict")
def predict(req: PredictRequest):
    results = run_dul_inference(req.telemetry, req.dul_model)
    return {"results": results}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    # v0.4: demo data only; v1.0 will query DB/fleet stats
    summary = [
        {"asset_id": "server-01", "avg_dul": 210, "worst_component": "SSD0"},
        {"asset_id": "server-02", "avg_dul": 60, "worst_component": "PSU1"},
    ]
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "summary": summary},
    )
