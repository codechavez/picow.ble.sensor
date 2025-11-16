import aioble
import ujson
import time
from mqtt_client import mqtt_publish
from networking import get_pico_mac

PICO_MAC = get_pico_mac()

async def run_ble_scanner():
    while True:
        async for result in aioble.scan(3000, interval_us=30000, window_us=30000):
            addr_type, addr = result.device.address()
            ble_mac = ':'.join(['{:02X}'.format(b) for b in addr])

            payload = {
                "sensor_mac": PICO_MAC,
                "ble_mac": ble_mac,
                "rssi": result.rssi,
                "timestamp": time.time()
            }

            mqtt_publish("sensors/ble", ujson.dumps(payload))


{
    "device": "E2:AA:BB:11:22:33",
    "sensor": "E2:AA:BB:11:22:33",
    "rssi": -65,
    "accuracy": 5.0,
    "x": 24.3,
    "y": 17.6,
    "distance": 29.7,
    "longitude": -121.893028,
    "latitude": 37.331822,
    "timestamp": "2025-11-13T19:48:21.842Z",
    "txPower": -10,
    "advertisementType": "iBeacon",
    "dataPayload": "0201061AFF4C000215FDA50693A4E24FB1AFCFC6EB076478250065080048C5"
}