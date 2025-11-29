from typing import Optional

import pandas as pd
from lifelines import CoxPHFitter

class SurvivalDULModel:
    """Cox proportional hazards survival model for failure risk / DUL."""

    def __init__(self):
        self.model: Optional[CoxPHFitter] = CoxPHFitter()

    def fit(self, df: pd.DataFrame, duration_col: str = "duration", event_col: str = "event"):
        self.model.fit(df, duration_col=duration_col, event_col=event_col)

    def hazard_ratio(self, df_features: pd.DataFrame):
        return self.model.predict_partial_hazard(df_features)

    def survival_function(self, df_features: pd.DataFrame):
        return self.model.predict_survival_function(df_features)
