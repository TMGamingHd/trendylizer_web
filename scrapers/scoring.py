import numpy as np
import pandas as pd
from utils.db import SessionLocal, TrendData, TrendScore
from scipy.stats import ttest_ind

def score_trends():
    """
    Fetch raw trend data from DB.
    Calculate composite scores combining velocity, engagement, novelty, saturation.
    Store in TrendScore table.
    """
    session = SessionLocal()

    # Get latest data grouped by trend_name
    query = session.query(TrendData.trend_name,
                          TrendData.timestamp,
                          TrendData.engagement).all()

    if not query:
        return

    df = pd.DataFrame(query, columns=["trend_name", "timestamp", "engagement"])

    scores = []
    for trend_name, group in df.groupby("trend_name"):
        group = group.sort_values("timestamp")

        # Velocity: rate of increase of engagement
        eng_diff = group.engagement.diff().fillna(0)
        velocity = eng_diff.mean()

        # Novelty: inverse of previous occurrence count
        novelty = 1.0 / (len(group) + 1)

        # Saturation: engagement relative to global max
        global_max = df.engagement.max()
        saturation = group.engagement.iloc[-1] / global_max if global_max > 0 else 0

        # Composite score: weighted sum (weights tunable)
        score = 0.5 * velocity + 0.3 * novelty + 0.2 * saturation

        scores.append((trend_name, score))

    # Save scores to DB
    for trend_name, score in scores:
        ts = TrendScore(trend_name=trend_name, score=score)
        session.add(ts)
    session.commit()
    session.close()


def main():
    score_trends()
