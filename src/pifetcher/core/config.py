from os import path
import json




class Config:
    browser = None
    queue = None
    logger = None
    fetcher = None
    @staticmethod
    def use_config(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)

            Config.browser = config["browser"]
            Config.queue = config["queue"]
            Config.logger = config["logger"]
            Config.fetcher = config["fetcher"]