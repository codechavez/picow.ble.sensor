import network
import time
import ujson

CONFIG_FILE = "config/device_config.json"

def load_config():
    with open(CONFIG_FILE) as f:
        return ujson.loads(f.read())

def wifi_connect(cfg):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(cfg["ssid"], cfg["password"])

    for _ in range(30):
        if wlan.isconnected():
            print("Wi-Fi connected:", wlan.ifconfig())
            return True
        time.sleep(0.5)
    return False
