
# ml/reinforcement_trainer.py
from ml.reward_model import score_generated_product

def fine_tune_generator_with_rewards(generated_texts):
    scored = [(text, score_generated_product(text)) for text in generated_texts]
    print("\n📊 Scored Outputs:")
    for text, score in scored:
        print(f"  ({score}) {text}")
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return [text for text, _ in ranked]
