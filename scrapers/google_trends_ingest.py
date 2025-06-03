from pytrends.request import TrendReq
from datetime import datetime
from utils.db import SessionLocal, TrendData
import logging

logger = logging.getLogger(__name__)

def ingest_google_trends(keywords, timeframe="now 7-d"):
    pytrends = TrendReq(hl='en-US', tz=360)
    session = SessionLocal()
    kw_list = keywords

    pytrends.build_payload(kw_list, timeframe=timeframe)
    interest_over_time_df = pytrends.interest_over_time()

    if interest_over_time_df.empty:
        logger.warning("No Google Trends data found")
        return

    count = 0
    for index, row in interest_over_time_df.iterrows():
        for kw in kw_list:
            value = row.get(kw)
            if value is not None and value > 0:
                data = TrendData(
                    source="google_trends",
                    trend_name=kw,
                    content="",
                    timestamp=index.to_pydatetime(),
                    engagement=value,
                )
                session.add(data)
                count += 1

    session.commit()
    session.close()
    logger.info(f"Ingested {count} Google Trends data points for {keywords}")

if __name__ == "__main__":
    ingest_google_trends(["AI", "blockchain"])


def main():
    ingest_google_trends()
