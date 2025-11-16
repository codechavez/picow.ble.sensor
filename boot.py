import json
import network
import time
import machine
import os

CONFIG_FILE = "config/device_config.json"

def load_config():
    if not CONFIG_FILE in os.listdir("config"):
        return None
    try:
        with open(CONFIG_FILE, "r") as config_file:
            return json.load(config_file)
    except:
        return None

def connect_wifi(cfg):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(cfg["ssid"], cfg["password"])

    for _ in range(30):
        if wlan.isconnected():
            return True
        time.sleep(0.5)
    return False

cfg = load_config()

if cfg:
    if connect_wifi(cfg):
        machine.nvs_setint("mode", 0)
    else:
        machine.nvs_setint("mode", 1)
else:
    machine.nvs_setint("mode", 1)
