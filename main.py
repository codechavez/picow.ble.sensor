import uasyncio as asyncio
import bluetooth
from config import load_config
from networking import connect_wifi, get_pico_mac
from mqtt_client import connect_mqtt, publish
from pairing import ble_pairing
from scanner import scan_and_publish

async def main():
    config = load_config()

    # BLE pairing if credentials missing
    if not config.get("wifi_ssid") or not config.get("wifi_password") or not config.get("mqtt_broker"):
        await ble_pairing(config)

    # Connect Wi-Fi
    if not connect_wifi(config["wifi_ssid"], config["wifi_password"]):
        print("Cannot continue without Wi-Fi")
        return

    # Connect MQTT
    pico_mac = get_pico_mac()
    if not connect_mqtt(pico_mac, config["mqtt_broker"], config.get("mqtt_port", 1883)):
        print("MQTT not connected, continuing anyway")

    # Start BLE scanning
    while True:
        await scan_and_publish()

asyncio.run(main())
