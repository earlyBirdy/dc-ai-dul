
import joblib
import torch
import os
from ai_dc_dul.models.dul_model import DULModel
from ai_dc_dul.models.sequence_dul_model import SequenceDULModel

def export_gbr(model: DULModel, path: str = "models/gbr_dul.pkl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model.model, path)
    return path

def export_lstm(model: SequenceDULModel, path: str = "models/lstm_dul.pt"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save(model.net.state_dict(), path)
    return path
