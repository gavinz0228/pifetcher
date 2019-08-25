from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
from os import path, getcwd, get_exec_path
from pifetcher.core import Config
from pifetcher.core import Logger
from pifetcher.utilities.data_utils import DataUtils

from sys import platform

if platform == 'win32':
    KEY_DRIVER_PATH = 'win-driver_path'
    KEY_BINARY_LOCATION = 'win-binary_location'
elif platform == "darwin":
    KEY_DRIVER_PATH = 'mac-driver_path'
    KEY_BINARY_LOCATION = 'mac-binary_location'
elif platform in ['linux','linux2']:
    KEY_DRIVER_PATH = 'linux-driver_path'
    KEY_BINARY_LOCATION = 'linux-binary_location'

def check_init(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        if not self.initialized:
            raise Exception("Dom is used before initializing.")
        return func(*args, **kwargs)
    return wrapper

class BaseDataFetcher(ABC):
    def __init__(self, config_file_path):

        # initialize browser
        options = Options()
        for option in Config.browser['browser_options']:
            options.add_argument(option)



        if path.exists(Config.browser[KEY_BINARY_LOCATION]):
            options.binary_location = Config.browser[KEY_BINARY_LOCATION]

        driver_abs_path = Config.browser[KEY_DRIVER_PATH]
        if not path.exists(Config.browser[KEY_DRIVER_PATH]):
            driver_abs_path = path.join(path.dirname(path.realpath(__file__)), '../','drivers/'+ Config.browser[KEY_DRIVER_PATH])
        if not path.exists(driver_abs_path):
            raise Exception(f"driver path {driver_abs_path} cannot be found")
        
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=driver_abs_path)

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
                value = self.get_value(val_config['selector'], val_config['type'], val_config['attribute'])
                if value:
                    parsed_data = True
            return_obj[field] = value
        return return_obj, parsed_data

    @check_init
    def get_value(self, path, type, attribute):
        element = self.dom.select_one(path)
        
        if not element:
            return None
        if attribute == ".text":
            return DataUtils.extract_by_type_name(element.text.strip(), type)
     
        elif attribute:
            return DataUtils.extract_by_type_name(element[attribute].strip() , type)
    
if __name__ == "__main__":
    pass
