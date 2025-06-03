
# ml/reward_model.py (extended)

import re
import math

def _keyword_score(text):
    keywords = ["eco", "AI", "remote", "green", "cyber"]
    return sum(1 for kw in keywords if kw.lower() in text.lower()) / len(keywords)

def _sentiment_simulation(text):
    # Simulate sentiment score: positive if contains good adjectives
    positive_words = ["great", "new", "innovative", "eco", "safe", "smart"]
    negative_words = ["risky", "expensive", "boring"]
    pos = sum(1 for w in positive_words if w in text.lower())
    neg = sum(1 for w in negative_words if w in text.lower())
    return max(min((pos - neg) / 3.0, 1.0), 0.0)

def _novelty_score(text):
    words = set(re.findall(r"\w+", text.lower()))
    return min(len(words) / 10.0, 1.0)

def score_generated_product(product_text):
    k = _keyword_score(product_text)
    s = _sentiment_simulation(product_text)
    n = _novelty_score(product_text)
    score = 0.4 * k + 0.4 * s + 0.2 * n
    return round(score, 3)
