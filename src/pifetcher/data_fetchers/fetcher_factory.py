from os import path

from pifetcher.core import Config
from pifetcher.data_fetchers import BaseDataFetcher, HttpRequestFetcher, PyppeteerFetcher
from pifetcher.utilities import SysUtils


class FetcherFactory:
    fetcher_cache = {}

    @staticmethod
    def get_fetcher_by_name(name):
        if name not in FetcherFactory.fetcher_cache:
            if name not in Config.fetcher['mappingConfigs']:
                raise ValueError(f'fetcher name {name} is not defined in the config file')

            fetcher_config_path = Config.fetcher['mappingConfigs'][name]
            if Config.driverType == 'HttpRequest':
                fetcher = HttpRequestFetcher(SysUtils.ensure_path(fetcher_config_path))
            elif Config.driverType == 'Pyppeteer':
                fetcher = PyppeteerFetcher(SysUtils.ensure_path(fetcher_config_path))
            else:
                fetcher = BaseDataFetcher(SysUtils.ensure_path(fetcher_config_path))

            FetcherFactory.fetcher_cache[name] = fetcher
        return FetcherFactory.fetcher_cache[name]
