from pifetcher.data_fetchers import BaseDataFetcher
from os import path
from pifetcher.core import Config

class FetcherFactory:
    fetcher_cache = {}
    @staticmethod
    def get_fetcher_by_name(name):
        if name not in FetcherFactory.fetcher_cache:
            fetcher = BaseDataFetcher(Config.fetcher['mappingConfigs'][name])
            FetcherFactory.fetcher_cache[name] = fetcher
        return FetcherFactory.fetcher_cache[name]
