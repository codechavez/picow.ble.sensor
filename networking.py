import network
import time

wlan = network.WLAN(network.STA_IF)

class WifiService:
    def __init__(self) -> None:
        pass
        
    def connect_wifi(ssid, password):        
        wlan.active(True)
        wlan.connect(ssid, password)
        for _ in range(20):
            if wlan.isconnected():
                ip, subnet, gateway, dns = wlan.ifconfig()
                print(f"Connected to Wi-Fi with IP Address: {ip}")
                return True
            time.sleep(1)
        print("Wi-Fi connection failed")
        return False

    def get_pico_mac():
            wlan.active(True)
            mac = wlan.config("mac")
            return ':'.join('{:02X}'.format(b) for b in mac)
