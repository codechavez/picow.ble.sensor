import uasyncio as asyncio
from config import load_config
from networking import connect_wifi
from mqtt_client import mqtt_connect
from ble_pairing import run_ble_pairing
from ble_scanner import run_ble_scanner
from networking import get_pico_mac

async def main():
    cfg = load_config()

    # Pairing required?
    if not cfg["wifi_ssid"] or not cfg["mqtt_host"]:
        print("No config found → pairing mode")
        await run_ble_pairing()
        cfg = load_config()

    # Connect Wi-Fi
    if not connect_wifi(cfg["wifi_ssid"], cfg["wifi_password"]):
        print("Wi-Fi failed → pairing again")
        await run_ble_pairing()
        cfg = load_config()
        connect_wifi(cfg["wifi_ssid"], cfg["wifi_password"])

    # Connect MQTT
    mqtt_connect(
        cfg["mqtt_host"],
        cfg["mqtt_port"],
        client_id=get_pico_mac().replace(":", "")
    )

    print("System ready → Starting BLE scanner...")
    await run_ble_scanner()

asyncio.run(main())
