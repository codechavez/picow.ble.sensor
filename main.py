import machine
import ujson
import asyncio

from ble_pairing.pairing import run_ble_pairing
from wifi.wifi_manager import wifi_connect, load_config
from mqtt.mqtt_manager import mqtt_connect
from scanner import run_ble_scanner


async def main():
    mode = machine.nvs_getint("mode") or 1

    if mode == 1:
        await run_ble_pairing()
    else:
        cfg = load_config()

        if not wifi_connect(cfg):
            machine.nvs_setint("mode", 1)
            machine.reset()

        client = mqtt_connect(cfg)
        if not client:
            machine.nvs_setint("mode", 1)
            machine.reset()

        await run_ble_scanner(client)

asyncio.run(main())
