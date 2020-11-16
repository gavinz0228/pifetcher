import json
import asyncio
from abc import ABC, abstractmethod
from os import path, getcwd, get_exec_path

from bs4 import BeautifulSoup
from pifetcher.core import Config
from pifetcher.utilities import DataUtils, SysUtils
from pyppeteer import launch

def check_init(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        if not self.initialized:
            raise Exception("Dom is used before initializing.")
        return func(*args, **kwargs)

    return wrapper


class PyppeteerFetcher(ABC):
    def __init__(self, config_file_path):

        # initialize browser
        self.browser = self.wait(launch({"headless": True, "handleSIGINT": False}))
        # initialize class variable
        self.html_source = None
        self.dom = None
        self.initialized = False
        self.config = self.load_config(config_file_path)

    def wait(self, coro):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)

    def load_html_by_url(self, url):
        page = self.wait(self.browser.newPage())
        self.wait(page.goto(url))
        self.html_source = self.wait(page.content())
        self.wait(page.close())
        self.dom = BeautifulSoup(self.html_source, 'html.parser')
        self.initialized = True
        return self.html_source

    def load_config(self, config_file_path):
        with open(config_file_path, 'r') as json_config:
            return json.load(json_config)

    def parse(self):
        return_obj = {}
        parsed_data = False

        for field, val_config in self.config.items():
            value, _ = self.get_value(val_config['selector'], val_config['type'], val_config['attribute'])
            if value:
                parsed_data = True
            return_obj[field] = value
        return return_obj, parsed_data

    def close(self):
        self.wait(self.browser.close())

    @check_init
    def get_value(self, path, type, attribute):
        element = self.dom.select_one(path)
        if not element:
            return None, f"element {path} was not found"
        if attribute == ".text":
            return DataUtils.extract_by_type_name(element.text.strip(), type)
        elif attribute:
            return DataUtils.extract_by_type_name(element[attribute].strip(), type)


if __name__ == "__main__":
    pass
