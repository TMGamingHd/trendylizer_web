import datetime
import pathlib
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


prompts = {
    "Trend Analysis": (
        "Summarize the latest trends, market drivers, and challenges shaping the {trend} sector in 2025. Highlight why now is an opportune moment to launch a new venture in this space."
    ),
    "Product Concept": (
        "Invent and detail a unique, high-potential product or service for {trend} that directly solves a pressing customer pain point. Describe its key features, value proposition, and differentiation from existing solutions."
    ),
    "Market Research & Validation": (
        "Provide a concise, data-backed validation plan for launching a {trend} business. Include target market size, main customer segments, competitor overview, and practical methods to test demand (such as surveys, interviews, or pilot programs)."
    ),
    "Product Development & Testing": (
        "Outline a phased roadmap for developing and testing an MVP (Minimum Viable Product) in {trend}. Include major milestones, feedback collection, and iteration strategies to ensure product-market fit."
    ),
    "Go-to-Market Strategy": (
        "Draft a go-to-market and launch strategy for a {trend} solution. Specify target customers, positioning, messaging, initial channels, and tactics to drive early user adoption."
    ),
    "Financial Plan": (
        "Create a 3-year financial projection for a {trend} startup, including estimated revenue streams, major cost categories, required funding, and anticipated break-even point."
    ),
    "Risks & Mitigation": (
        "List the top risks and obstacles that could impact a {trend} startup, and propose actionable strategies to mitigate or overcome each risk."
    ),
    "Future Roadmap": (
        "Propose a 3-year company and product roadmap for growth and innovation in the {trend} space. Highlight key expansion milestones, upcoming feature releases, and scaling strategies."
    ),
    "About Our Company": (
        "Write a concise, mission-driven company profile for a {trend} venture. Emphasize vision, core values, leadership, and commitment to positive industry impact."
    )
}
def ai_generate_section(prompt):
    return query_model("ebook_section", prompt)

def generate_ebook(trend, author="Trendylizer AI", website="https://trendylizer.ai"):
    today = datetime.date.today()
    title = f"Business Blueprint: Launching a {trend.capitalize()} Venture in 2025"
    subtitle = f"From Idea to Execution — A Business Plan Centered on {trend.capitalize()}"
    date_str = today.strftime("%B %d, %Y")
    trend_slug = "".join(c.lower() if c.isalnum() else "_" for c in trend).strip("_")
    img_dir = f"outputs/ebook"

    metadata = f"""---
title: "{title}"
author: "{author}"
date: "{date_str}"
keywords: {trend}
---

"""
    title_page = f"""# {title}

## {subtitle}

**Published by:** {author}  
**Website:** {website}  
**Date:** {date_str}

---
"""

    copyright_page = f"""**Copyright © {today.year} {author}. All rights reserved.**

---
"""

    product_concept_text = ""
    sections = []
    for section_title, section_prompt in prompts.items():
        prompt = section_prompt.format(trend=trend)
        section_content = ai_generate_section(prompt)
        if isinstance(section_content, list):
            section_content = "\n".join(str(x) for x in section_content)
        elif not isinstance(section_content, str):
            section_content = str(section_content)
        # Add image to Product Concept section only (customize as you wish)
        if section_title == "Product Concept":
            product_concept_text = section_content
            image_prompt = f"Create a visually compelling, modern illustration for a business plan featuring: {section_content}"
            image_filename = f"{img_dir}/img_{trend_slug}_concept.png"
            img_path = ai_generate_image(image_prompt, image_filename)
            section_content += f"\n\n![Product Concept Illustration]({img_path})"
        sections.append(f"# {section_title}\n\n{section_content}\n---\n")

    cta = f"""# Call to Action

Want your own trend-based business plan?  
Contact us at [{website}]({website}).

---
"""

    ebook = (
        metadata +
        title_page +
        copyright_page +
        "".join(sections) +
        cta
    )

    return ebook, product_concept_text
