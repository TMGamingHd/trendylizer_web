
# generators/marketing_generator.py
import random

def generate_ebook_outline(trend_keywords):
    outline = ["Introduction", "Trend Overview"]
    for kw in trend_keywords:
        outline.append(f"Chapter: {kw}")
    outline.append("Conclusion")
    return outline

def generate_ad_copy(trend_keywords):
    templates = [
        "Introducing our product inspired by {}!",
        "New launch: {} is the future!",
        "Join the {} revolution today.",
        "Discover innovation with {}.",
        "Why {} is your next smart move."
    ]
    ads = []
    for kw in trend_keywords:
        tmpl = random.choice(templates)
        ads.append(tmpl.format(kw.replace("_", " ").title()))
    return ads

def generate_infographic_ideas(trend_keywords):
    return [f"Infographic: The rise of {kw}" for kw in trend_keywords]
