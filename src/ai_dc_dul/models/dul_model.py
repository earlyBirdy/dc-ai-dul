from typing import Optional

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

class DULModel:
    """Gradient boosting regression model for Depreciation Useful Life (DUL)."""

    def __init__(self, random_state: int = 42):
        self.model: Optional[GradientBoostingRegressor] = GradientBoostingRegressor(
            random_state=random_state
        )

    def fit(self, X, y) -> float:
        self.model.fit(X, y)
        y_pred = self.model.predict(X)
        mae = mean_absolute_error(y, y_pred)
        return mae

    def predict(self, X) -> np.ndarray:
        return self.model.predict(X)
