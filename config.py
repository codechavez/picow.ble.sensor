import ujson, os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "wifi_ssid": None,
    "wifi_password": None,
    "mqtt_host": None,
    "mqtt_port": 1883
}

def load_config():
    if CONFIG_FILE not in os.listdir():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    with open(CONFIG_FILE, "r") as f:
        return ujson.loads(f.read())

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        f.write(ujson.dumps(cfg))
