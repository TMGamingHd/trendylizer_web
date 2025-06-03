import os
import tweepy
from datetime import datetime, timedelta
from utils.db import SessionLocal, TrendData
from scrapers.config import Config
import logging

logger = logging.getLogger(__name__)

def ingest_twitter(keywords, max_tweets=100):
    """
    Collect recent tweets matching keywords.
    Store results in DB table TrendData.
    """
    client = tweepy.Client(
        bearer_token=config.TWITTER_BEARER_TOKEN,
        wait_on_rate_limit=True,
    )
    session = SessionLocal()

    query = " OR ".join(keywords) + " lang:en -is:retweet"
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)

    tweets = tweepy.Paginator(
        client.search_recent_tweets,
        query=query,
        tweet_fields=['created_at', 'public_metrics', 'text'],
        start_time=start_time.isoformat("T") + "Z",
        end_time=end_time.isoformat("T") + "Z",
        max_results=100,
    ).flatten(limit=max_tweets)

    count = 0
    for tweet in tweets:
        data = TrendData(
            source="twitter",
            trend_name=",".join(keywords),
            content=tweet.text,
            timestamp=tweet.created_at,
            engagement=tweet.public_metrics.get('like_count',0)+
                       tweet.public_metrics.get('retweet_count',0)+
                       tweet.public_metrics.get('reply_count',0),
        )
        session.add(data)
        count += 1

    session.commit()
    session.close()
    logger.info(f"Ingested {count} tweets for keywords {keywords}")

if __name__ == "__main__":
    ingest_twitter(["AI", "ChatGPT"], max_tweets=50)


def main():
    ingest_twitter()
