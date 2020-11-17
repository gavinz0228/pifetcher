import json
from os import path


class Config:
    initialized = False
    browser = None
    queue = None
    logger = None
    fetcher = None

    @staticmethod
    def use(config_path):
        if not path.exists(config_path):
            raise Exception(f'config file path does not exist. please create one')
        with open(config_path, 'r') as f:
            config = json.load(f)

            Config.queue = config.get("queue", "LocalWorkQueue")
            Config.logger = config.get("logger", "console")
            Config.fetcher = config["fetcher"]
            Config.driverType = config.get("driverType", "pyppeteer")
            Config.initialized = True
