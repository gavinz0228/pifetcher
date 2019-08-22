from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def check_init(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        if not self.initialized:
            raise Exception("Dom is used before initializing.")
        func(*args, **kwargs)
    return wrapper


class BaseDataFetcher(ABC):
    def __init__(self):
        # initialize browser
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options, executable_path="bin/chromedriver.exe")
        #initialize class variable
        self.html_source = None
        self.dom = None
        self.initialized = False
    def load_html_by_url(self, url):
        self.driver.get(url)
        self.html_source = self.driver.page_source
        self.dom = BeautifulSoup(self.html_source, 'html.parser')
        self.initialized = True
        return self.html_source

    @check_init
    def select_text(self, path):
        return self.dom.select_one(path).text

