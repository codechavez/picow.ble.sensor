import ujson
import aioble
import uasyncio as asyncio
import bluetooth

from config import save_config

PAIR_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
RX_UUID   = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
TX_UUID   = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

async def ble_pairing(config):
    print("Starting BLE pairing mode...")
    async with aioble.Service(PAIR_UUID) as service:
        async with service.characteristic(RX_UUID) as rx:
            while True:
                data = await rx.read()
                if not data:
                    continue
                try:
                    payload = ujson.loads(data)
                    ssid = payload.get("wifi_ssid")
                    password = payload.get("wifi_password")
                    broker = payload.get("mqtt_broker")
                    port = payload.get("mqtt_port", 1883)
                    if ssid and password and broker:
                        config.update({
                            "wifi_ssid": ssid,
                            "wifi_password": password,
                            "mqtt_broker": broker,
                            "mqtt_port": port
                        })
                        save_config(config)
                        print("Credentials saved!")
                        return
                except Exception as e:
                    print("Invalid BLE payload:", e)
