from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
from os import path

BROWSER_CONFIG_FILE_PATH = 'config.json'

def check_init(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        if not self.initialized:
            raise Exception("Dom is used before initializing.")
        return func(*args, **kwargs)
    return wrapper


class BaseDataFetcher(ABC):
    def __init__(self, config_file_path):

        #load browser config
        browser_config_path = path.join(path.dirname(path.realpath(__file__)), '../', BROWSER_CONFIG_FILE_PATH)
        browser_config = None 
        with open(browser_config_path, 'r') as f:
            browser_config = json.load(f)

        # initialize browser
        options = Options()
        for option in browser_config['browser_options']:
            options.add_argument(option)

        self.driver = webdriver.Chrome(chrome_options=options, executable_path="bin/chromedriver.exe")
        #initialize class variable
        self.html_source = None
        self.dom = None
        self.initialized = False
        self.config = self.load_config(config_file_path)

    def load_html_by_url(self, url):
        self.driver.get(url)
        self.html_source = self.driver.page_source
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
            value = None
            if val_config['type'] == 'text':
                value = self.select_text(val_config['selector'])
                if value:
                    parsed_data = True

            return_obj[field] = value
        return return_obj, parsed_data

    @check_init
    def select_text(self, path):
        element = self.dom.select_one(path)
        if element:
            return element.text
        else:
            return None


