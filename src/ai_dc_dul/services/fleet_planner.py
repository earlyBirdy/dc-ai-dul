from datetime import datetime, timedelta
import pandas as pd
import sqlalchemy as sa

class FleetPlanner:
    def __init__(self, db_uri: str):
        self.db = sa.create_engine(db_uri)

    def load_latest_predictions(self):
        query = '''
        SELECT DISTINCT ON (asset_id, component_id)
            asset_id, component_id, dul_pred_days, anomaly_score, ts
        FROM dul_predictions
        ORDER BY asset_id, component_id, ts DESC
        '''
        return pd.read_sql(query, self.db)

    def calculate_risk(self, days: float):
        if days < 30:
            return "red"
        elif days < 90:
            return "orange"
        return "green"

    def generate_plan(self):
        df = self.load_latest_predictions()
        today = datetime.utcnow().date()

        rows = []
        for _, row in df.iterrows():
            remaining = float(row["dul_pred_days"])
            risk = self.calculate_risk(remaining)
            replacement_date = today + timedelta(days=remaining)

            rows.append({
                "asset_id": row.asset_id,
                "component_id": row.component_id,
                "predicted_dul": remaining,
                "risk_level": risk,
                "replacement_date": str(replacement_date),
                "capex_estimate": 200.0,
            })

        return pd.DataFrame(rows)

    def store_plan(self, df_plan):
        df_plan["generated_at"] = datetime.utcnow()
        df_plan.to_sql("planner_output", self.db, if_exists="append", index=False)
