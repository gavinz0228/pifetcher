import logging
from pifetcher.core import Config

logging.basicConfig(level=logging.WARNING)

if Config.logger["output"] == "console":
    pass

class Logger:
    @staticmethod
    def debug(msg):
        logging.debug(msg)
    @staticmethod
    def info(msg):
        logging.info(msg)
    @staticmethod
    def warning(msg):
        logging.warning(msg)