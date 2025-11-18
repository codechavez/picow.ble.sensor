import time
from scanner import BleScanner
import uasyncio as asyncio
from config import load_config
from networking import connect_wifi, get_pico_mac
from mqtt_client import connect_mqtt, publish
from pairing import ble_pairing
import bluetooth

async def main():
    pico_mac = get_pico_mac()
    print(f'Pico MAC Address: {pico_mac}')
    
    config = load_config()
    print("Loaded config:", config)
    
    # BLE pairing if credentials missing
    if not config.get("wifi_ssid") or not config.get("wifi_password") or not config.get("mqtt_broker"):
        await ble_pairing(config)
        
    # Connect Wi-Fi
    if not connect_wifi(config["wifi_ssid"], config["wifi_password"]):
        print("Cannot continue without Wi-Fi")
        return
    
    # Connect MQTT
    if not connect_mqtt(pico_mac, config["mqtt_broker"], config.get("mqtt_port", 30183)):
        print("MQTT not connected, continuing anyway")
        return

    # Start BLE scanning
    ble = bluetooth.BLE()
    scanner = BleScanner(ble)
    
    while True:
        scanner.start_scan(5000)
        time.sleep(30)

asyncio.run(main())
