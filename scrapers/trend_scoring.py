import numpy as np
from utils.db import SessionLocal, ProcessedTrendFeature, TrendScore
from datetime import datetime
from scipy.stats import mannwhitneyu

def compute_score(trend_id, current_count, prev_window_count, engagement, novelty_days, commercial_potential, saturation):
    w_velocity = 0.3
    w_engagement = 0.3
    w_novelty = 0.2
    w_mon = 0.2
    w_sat = 0.1

    V = (current_count - prev_window_count) / (prev_window_count + 1e-5)
    E = engagement
    N = 1 / (novelty_days + 1)
    M = commercial_potential
    S = saturation

    base_score = w_velocity * V + w_engagement * E + w_novelty * N + w_mon * M - w_sat * S
    return base_score

def test_significance(current_counts, baseline_counts):
    stat, p = mannwhitneyu(current_counts, baseline_counts, alternative='greater')
    return p

def score_trends():
    session = SessionLocal()
    # Example: get processed features grouped by trend_id
    features = session.query(ProcessedTrendFeature).all()

    # Placeholder logic
    for feat in features:
        current_count = 100  # dummy
        prev_count = 80  # dummy
        engagement = 50  # dummy
        novelty_days = 3  # dummy
        commercial_potential = 0.7  # dummy
        saturation = 0.3  # dummy

        score = compute_score(feat.trend_id, current_count, prev_count, engagement, novelty_days, commercial_potential, saturation)

        # Hypothesis testing with dummy counts
        p_val = test_significance([current_count], [prev_count])
        significant = p_val < 0.05
        if not significant:
            score *= 0.5

        trend_score = TrendScore(
            trend=f"trend_{feat.trend_id}",
            score=score,
            significance=significant,
            computed_at=datetime.utcnow(),
        )
        session.add(trend_score)

    session.commit()
    session.close()


def main():
    compute_score()
