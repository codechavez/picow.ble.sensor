import aioble
import ujson
import time
import asyncio

TOPIC = b"devices/picow/ble"

async def run_ble_scanner(client):
    print("BLE scanning started")

    while True:
        async with aioble.scan(timeout_ms=4000) as scanner:
            async for adv in scanner:
                payload = ujson.dumps({
                    "mac": adv.device_addr,
                    "rssi": adv.rssi,
                    "ts": time.time()
                })
                client.publish(TOPIC, payload)
        await asyncio.sleep(1)
