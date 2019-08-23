from os import path
import json

CONFIG_FILE_PATH = 'config.json'
config_path = path.join(path.dirname(path.realpath(__file__)), CONFIG_FILE_PATH)
config = None

with open(config_path, 'r') as f:
    config = json.load(f)

class Config:
    browser = config["browser"]
    worker = config["worker"]
