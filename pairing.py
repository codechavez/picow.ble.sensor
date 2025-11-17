import aioble
import time
import ujson
import uasyncio as asyncio
from machine import Pin, reset
from bluetooth import UUID
from config import save_config
from networking import get_pico_mac

PAIR_UUID = UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
RX_UUID   = UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
TX_UUID   = UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

led = Pin("LED", Pin.OUT)
PAIRING_TIMEPOUT = 180

# -------------------------------------------------------
# LED BLINK PATTERNS
# -------------------------------------------------------
async def led_pairing_pattern():
    """
    Slow blink: pairing mode active.
    Runs as a background task until cancelled.
    """
    while True:
        led.on()
        await asyncio.sleep(1)
        led.off()
        await asyncio.sleep(0.4)

async def led_connected_flash():
    while True:
        led.on()
        await asyncio.sleep(0.1)
        led.off()
        await asyncio.sleep(0.1)

# -------------------------------------------------------
# BLE PAIRING LOGIC
# -------------------------------------------------------
async def ble_pairing(config):
    print("Starting BLE pairing mode...")

    pairing_task = asyncio.create_task(led_pairing_pattern())

    service = aioble.Service(PAIR_UUID)

    rx_char = aioble.Characteristic(
        service, RX_UUID,
        write=True
    )

    tx_char = aioble.Characteristic(
        service, TX_UUID,
        notify=True
    )

    aioble.register_services(service)

    adv_task = asyncio.create_task(
        aioble.advertise(
            interval_us=20_000,
            name=f"PicoW {get_pico_mac()}",
            services=[PAIR_UUID]
        )
    )
    
    print("Waiting for BLE connection...")

    try:
        connection = await asyncio.wait_for(adv_task, 180)
        pairing_task.cancel()
        print("BLE device connected")
        await led_connected_flash()
    except asyncio.TimeoutError:
        print("PAIRING TIMEOUT → restarting")
        pairing_task.cancel()
        adv_task.cancel()
        reset()
        return

    while True:
        try:
            await connection.wait_for_write(rx_char)
            raw = rx_char.read().decode()
            print("Received:", raw)

            try:
                new_cfg = ujson.loads(raw)
            except:
                print("Invalid JSON received")
                continue

            # Validate required keys
            if not ("wifi_ssid" in new_cfg and
                    "wifi_password" in new_cfg and
                    "mqtt_broker" in new_cfg):
                print("Missing required values")
                continue

            save_config(new_cfg)
            print("Config saved!")

            tx_char.write(b"OK")
            await tx_char.notify(connection)

            pairing_task.cancel()
            reset()
            return

        except Exception as err:
            print("BLE pairing error:", err)
            break
