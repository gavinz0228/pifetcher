import aiohttp
import asyncio
from bs4 import BeautifulSoup
from core.base_data_fetcher import BasePriceFetcher 


class AmazonPriceTracker(BasePriceFetcher):
    def __init__(self, *args, **kwargs):
        super(AmazonPriceTracker, self).__init__(*args, **kwargs)
        
    def get_price(self):
        return self.parse_text('#priceblock_ourprice')

