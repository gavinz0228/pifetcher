from abc import ABC, abstractmethod
from base_data_fetcher import BaseDataFetcher

class BasePriceFetcher(BaseDataFetcher):
    def __init__(self):
        super(BasePriceFetcher, self).__init__(*args, **kwargs)
    def get(self, url):
        return self.load_html_by_url(url)
    @abstractmethod
    def get_price(self, path):
        raise NotImplementedError()
