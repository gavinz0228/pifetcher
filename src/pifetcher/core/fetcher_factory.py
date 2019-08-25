from pifetcher.data_fetchers import BaseDataFetcher
from os import path

class FetcherFactory:
    fetcher_cache = {}
    @staticmethod
    def get_fetcher_by_name(name):
        if name not in FetcherFactory.fetcher_cache:
            rel_path = '../fetcher_configs/' + name + '.json'
            fetcher = BaseDataFetcher(path.join(path.dirname(path.realpath(__file__)), rel_path))
            FetcherFactory.fetcher_cache[name] = fetcher
        return FetcherFactory.fetcher_cache[name]
