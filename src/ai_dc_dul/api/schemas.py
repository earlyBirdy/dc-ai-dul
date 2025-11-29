from typing import Dict, List, Literal, Optional
from datetime import datetime
from pydantic import BaseModel

ComponentType = Literal["psu", "fan", "ssd", "cpu", "gpu", "memory", "nic", "rack_env"]

class TelemetryInput(BaseModel):
    ts: datetime
    asset_id: str
    component_id: str
    component_type: ComponentType
    vendor: Optional[str] = None
    model: Optional[str] = None
    metrics: Dict[str, float]

class PredictRequest(BaseModel):
    telemetry: List[TelemetryInput]
    dul_model: Literal["gbr", "lstm"] = "gbr"
