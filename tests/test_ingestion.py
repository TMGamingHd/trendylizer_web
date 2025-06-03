import pytest
from scrapers.twitter_ingest import ingest_twitter

def test_twitter_ingest_runs():
    # This test only checks that function runs without error
    ingest_twitter(["AI"], max_tweets=5)
    assert True

# Similar tests for other ingestion modules...
