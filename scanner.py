import uasyncio as asyncio
import ujson
import aioble
import time
from mqtt_client import publish
from networking import get_pico_mac
from machine import Pin
from config import load_config


# LED pin
led = Pin("LED", Pin.OUT)

async def blink_led(duration=0.1):
    led.on()
    await asyncio.sleep(duration)
    led.off()

async def scan_and_publish():
    config = load_config()
    pico_mac = get_pico_mac()
    while True:
        devices = await aioble.scan(5_000)  # scan 5 sec
        timestamp = time.time()
        for dev in devices:
            print("Found device:", dev.addr.hex(), "RSSI:", dev.rssi)
            payload = ujson.dumps({
                "sensor_mac": pico_mac,
                "ble_mac": dev.addr.hex(),  # BLE MAC as string
                "rssi": dev.rssi,
                "timestamp": timestamp
            })
            publish(config["topic"], payload)
            asyncio.create_task(blink_led())  
            
        await asyncio.sleep(5)


# {
#     "device": "E2:AA:BB:11:22:33",
#     "sensor": "E2:AA:BB:11:22:33",
#     "rssi": -65,
#     "accuracy": 5.0,
#     "x": 24.3,
#     "y": 17.6,
#     "distance": 29.7,
#     "longitude": -121.893028,
#     "latitude": 37.331822,
#     "timestamp": "2025-11-13T19:48:21.842Z",
#     "txPower": -10,
#     "advertisementType": "iBeacon",
#     "dataPayload": "0201061AFF4C000215FDA50693A4E24FB1AFCFC6EB076478250065080048C5"
# }