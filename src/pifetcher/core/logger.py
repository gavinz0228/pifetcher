import logging
from pifetcher.core import Config



class Logger:
    initialized = False
    @staticmethod
    def init():
        if Logger.initialized == False:
            logging.basicConfig(level=logging.WARNING)
    
    @staticmethod
    def debug(msg):
        Logger.init()
        logging.debug(msg)
    @staticmethod
    def info(msg):
        Logger.init()
        logging.info(msg)
    @staticmethod
    def warning(msg):
        Logger.init()
        logging.warning(msg)
    @staticmethod
    def error(msg):
        Logger.init()
        logging.error(msg)