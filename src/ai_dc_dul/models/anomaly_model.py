from typing import Optional
import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyModel:
    """Simple anomaly detector using IsolationForest."""

    def __init__(self, random_state: int = 42):
        self.model: Optional[IsolationForest] = IsolationForest(
            contamination="auto",
            n_estimators=200,
            random_state=random_state,
        )

    def fit(self, X):
        self.model.fit(X)

    def anomaly_score(self, X):
        raw = self.model.score_samples(X)
        raw = np.array(raw)
        min_v, max_v = raw.min(), raw.max()
        if max_v - min_v < 1e-9:
            return np.zeros_like(raw)
        norm = (max_v - raw) / (max_v - min_v)
        return norm
