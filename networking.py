import network
import time

wlan = network.WLAN(network.STA_IF)

def get_pico_mac():
    wlan.active(True)
    mac = wlan.config("mac")
    return ':'.join('{:02X}'.format(b) for b in mac)


def connect_wifi(ssid, password):
    wlan.active(True)
    wlan.connect(ssid, password)

    for _ in range(30):
        if wlan.isconnected():
            return True
        time.sleep(1)

    return False
