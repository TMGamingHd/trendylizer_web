from llm_router import query_model
import os
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw

load_dotenv()

def ai_generate_image(prompt, filename):
    api_key = os.getenv("SD_API_KEY")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    api_url = "https://modelslab.com/api/v6/realtime/text2img"
    payload = {
        "key": api_key,
        "prompt": prompt,
        "negative_prompt": "",
        "width": "512",
        "height": "512",
        "samples": 1,
        "safety_checker": False,
        "seed": None,
        "base64": False,
        "webhook": None,
        "track_id": None
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        if 'output' in result and result['output']:
            img_url = result['output'][0]
            img_data = requests.get(img_url).content
            with open(filename, 'wb') as f:
                f.write(img_data)
            return filename
        else:
            raise ValueError("No output URL in response.")
    except Exception as e:
        print(f"[ModelsLab ERROR]: {e}. Generating placeholder image.")
        # Create a placeholder image locally
        image = Image.new('RGB', (512, 512), color=(240, 240, 240))
        draw = ImageDraw.Draw(image)
        draw.text((10, 250), "No Image", fill=(0, 0, 0))
        image.save(filename)
        return filename

ad_copy_prompts = {
    "Headline": (
        "Given the following product idea, write a compelling, punchy ad headline for this product, targeted at decision makers in 2025. Product Idea:\n\n{product_idea}\n"
    ),
    "Body": (
        "Given the following product idea, write persuasive ad body copy explaining its main benefits and unique features. Focus on how it helps customers solve their most important pain points in 2025. Product Idea:\n\n{product_idea}\n"
    ),
    "Call to Action": (
        "Given the following product idea, write a strong, actionable call-to-action for this marketing campaign. Product Idea:\n\n{product_idea}\n"
    )
}

def ai_generate_ad_section(prompt):
    return query_model("ad_copy_section", prompt)

def ai_improve_ad_copy(raw_ad_copy, product_idea):
    improve_prompt = (
    f"The following is a draft of an ad copy focused on the {product_idea} product:\n\n"
    f"{raw_ad_copy}\n\n"
    "Please rewrite this ad copy to significantly improve its clarity, persuasiveness, and professionalism. "
    "Refine the messaging to better resonate with target decision-makers in 2025, enhancing emotional appeal, value proposition, and strategic relevance. "
    "Ensure the tone is confident and forward-looking, and that the structure flows logically from headline to body to call-to-action. "
    "Deliver the optimized version in polished markdown format, clearly dividing each section with appropriate headers (e.g., ## Headline, ## Body, ## Call to Action). "
    "Feel free to propose alternate headline options if relevant, and briefly explain any significant creative choices made."
)
    return query_model("ad_copy_improvement", improve_prompt)

def generate_ad_copy(trend, product_idea, author="Trendylizer AI"):
    trend_slug = "".join(c.lower() if c.isalnum() else "_" for c in trend).strip("_")
    img_dir = f"outputs/ebook"
    parts = []
    parts.append(f"# Ad Copy for {trend.capitalize()}\n")
    for section, prompt in ad_copy_prompts.items():
        filled_prompt = prompt.format(product_idea=product_idea)
        content = ai_generate_ad_section(filled_prompt)
        if isinstance(content, list):
            content = "\n".join(str(x) for x in content)
        elif not isinstance(content, str):
            content = str(content)
        # Add image to Headline section only (customize as you wish)
        if section == "Headline":
            image_prompt = f"Create a modern, attention-grabbing ad image for the following product: {product_idea}"
            image_filename = f"{img_dir}/img_{trend_slug}_ad_headline.png"
            img_path = ai_generate_image(image_prompt, image_filename)
            content += f"\n\n![Ad Headline Image]({img_path})"
        parts.append(f"## {section}\n{content}\n")
    raw_ad_copy_md = "\n".join(parts)
    improved_ad_copy = ai_improve_ad_copy(raw_ad_copy_md, product_idea)
    if not improved_ad_copy:
        improved_ad_copy = raw_ad_copy_md  # fallback
    improved_ad_copy += f"\n---\n*Created by {author}*"
    return improved_ad_copy
