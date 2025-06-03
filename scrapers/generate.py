# src/content_pipeline/generate.py
import os
import datetime
from fpdf import FPDF
import requests
from notion_client import Client as NotionClient
from typing import List, Dict

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

class EbookGenerator:
    def __init__(self, title: str, author: str = "Trend2Product Bot"):
        self.title = title
        self.author = author
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def add_title_page(self):
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 24)
        self.pdf.cell(0, 10, self.title, ln=True, align="C")
        self.pdf.set_font("Arial", "", 16)
        self.pdf.cell(0, 10, f"By {self.author}", ln=True, align="C")
        self.pdf.cell(0, 10, datetime.datetime.now().strftime("%B %d, %Y"), ln=True, align="C")

    def add_section(self, heading: str, content: str):
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 18)
        self.pdf.multi_cell(0, 10, heading)
        self.pdf.set_font("Arial", "", 12)
        self.pdf.multi_cell(0, 10, content)

    def save(self, filepath: str):
        self.pdf.output(filepath)

class NotionPublisher:
    def __init__(self):
        if not NOTION_TOKEN or not NOTION_DATABASE_ID:
            raise Exception("Missing NOTION_TOKEN or NOTION_DATABASE_ID env vars.")
        self.client = NotionClient(auth=NOTION_TOKEN)
        self.database_id = NOTION_DATABASE_ID

    def publish_trend(self, trend: Dict):
        # A simple page creation example
        new_page = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {"title": [{"text": {"content": trend.get("title", "Untitled Trend")}}]},
                "Date": {"date": {"start": datetime.datetime.now().isoformat()}}
            },
            "children": [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"text": [{"type": "text", "text": {"content": "Summary"}}]},
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"text": [{"type": "text", "text": {"content": trend.get("summary", "")}}]},
                },
                # Add more structured content as needed
            ],
        }
        response = self.client.pages.create(**new_page)
        return response

def generate_ebook_from_trends(trends: List[Dict], output_path: str):
    ebook = EbookGenerator("Emerging Trends Report")
    ebook.add_title_page()
    for trend in trends:
        heading = trend.get("title", "Untitled")
        content = trend.get("summary", "No summary available.")
        ebook.add_section(heading, content)
    ebook.save(output_path)

def publish_trends_to_notion(trends: List[Dict]):
    publisher = NotionPublisher()
    responses = []
    for trend in trends:
        resp = publisher.publish_trend(trend)
        responses.append(resp)
    return responses


def main():
    __init__()
