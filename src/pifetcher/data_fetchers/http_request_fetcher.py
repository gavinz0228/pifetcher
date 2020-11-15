import json
from abc import ABC, abstractmethod
from os import path, getcwd, get_exec_path

from bs4 import BeautifulSoup
from pifetcher.core import Config
from pifetcher.utilities import DataUtils, SysUtils
import requests

def check_init(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        if not self.initialized:
            raise Exception("Dom is used before initializing.")
        return func(*args, **kwargs)

    return wrapper

default_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Referer": "https://www.amazon.com/",
    "Origin": "https://www.amazon.com/",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Connection": "keep-alive",
    "Content-Length": "2588",
    "Content-Type": "text/plain;charset=UTF-8"
    }

class HttpRequestFetcher(ABC):
    def __init__(self, config_file_path):
        self.html_source = None
        self.dom = None
        self.initialized = False
        self.config = self.load_config(config_file_path)

    def load_html_by_url(self, url):
        self.html_source = requests.get(url, default_headers).text
        print(self.html_source)
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
        pass

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
