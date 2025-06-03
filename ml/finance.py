import requests
import logging
from src.utils.config import config

logger = logging.getLogger(__name__)

class FinanceIngestor:
    def __init__(self):
        self.api_key = config.FINANCE_API_KEY
        self.base_url = "https://financialmodelingprep.com/api/v3"

    def get_stock_quotes(self, symbols):
        try:
            symbols_str = ",".join(symbols)
            url = f"{self.base_url}/quote/{symbols_str}?apikey={self.api_key}"
            resp = requests.get(url)
            data = resp.json()
            return data
        except Exception as e:
            logger.error(f"Finance fetch error: {e}")
            return []
