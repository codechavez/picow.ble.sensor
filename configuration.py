import ujson
import os

CONFIG_FILE = "config.json"

def load_config():
    if CONFIG_FILE in os.listdir():
        with open(CONFIG_FILE, "r") as f:
            return ujson.load(f)
    else:
        return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        ujson.dump(data, f)
