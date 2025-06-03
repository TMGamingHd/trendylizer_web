import praw
import json
import os
from datetime import datetime
from utils.db import SessionLocal, RawTrendData
from scrapers.config import Config
from utils.logger import get_logger

logger = get_logger("reddit_ingest")

def ingest_reddit(subreddits=["all"], limit=100):
    reddit = praw.Reddit(
        client_id=Config.REDDIT_CLIENT_ID,
        client_secret=Config.REDDIT_CLIENT_SECRET,
        user_agent=Config.REDDIT_USER_AGENT,
    )
    session = SessionLocal()
    all_data = []

    for subreddit in subreddits:
        subreddit_obj = reddit.subreddit(subreddit)
        for submission in subreddit_obj.hot(limit=limit):
            data = {
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext,
                "score": submission.score,
                "url": submission.url,
                "num_comments": submission.num_comments,
                "created_utc": submission.created_utc,
                "subreddit": subreddit,
            }
            all_data.append(data)

            # Save raw to DB
            raw = RawTrendData(
                source="reddit",
                raw_json=data,
                timestamp=datetime.utcfromtimestamp(submission.created_utc),
            )
            session.add(raw)

    session.commit()
    session.close()

    # Save raw JSON to disk
    os.makedirs("data/raw/reddit", exist_ok=True)
    filename = f"data/raw/reddit/reddit_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)

    logger.info(f"Reddit ingestion complete: {len(all_data)} records saved.")
    return all_data

if __name__ == "__main__":
    ingest_reddit()



def main():
    ingest_reddit()
