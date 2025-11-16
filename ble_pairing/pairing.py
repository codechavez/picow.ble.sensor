import aioble
import machine
import ujson
import time
import os

CONFIG_FILE = "config/device_config.json"

PAIR_UUID = aioble.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
RX_UUID   = aioble.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")

def save_config(obj):
    if not "config" in os.listdir():
        os.mkdir("config")

    with open(CONFIG_FILE, "w") as f:
        f.write(ujson.dumps(obj))


async def run_ble_pairing():
    service = aioble.Service(PAIR_UUID)
    rx = aioble.Characteristic(service, RX_UUID, write=True, write_no_response=True)
    aioble.register_services(service)

    adv = aioble.advertise(100_000, name="PicoW-Setup", services=[PAIR_UUID])
    print("PAIRING MODE: waiting for credentials...")

    async with adv:
        while True:
            conn = await aioble.accept()
            print("BLE connected")

            try:
                while True:
                    data = await rx.written()
                    print("Received:", data)

                    try:
                        obj = ujson.loads(data)
                        save_config(obj)
                        print("Saved configuration")
                        time.sleep(1)
                        machine.reset()
                    except:
                        print("Invalid JSON")
            except:
                pass
                