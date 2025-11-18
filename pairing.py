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

async def handle_rx(rx_char):
    buf = b""
    print("Waiting for RX write...")

    async for chunk in rx_char.written():
        print("Chunk:", chunk)
        buf += chunk

        try:
            msg = buf.decode()
            data = ujson.loads(msg)
            print("Received full JSON:", data)
            buf = b""     # clear after success
        except ValueError:
            # not complete yet
            pass

# -------------------------------------------------------
# BLE PAIRING LOGIC
# -------------------------------------------------------
async def ble_pairing(config):
    print("Starting BLE pairing mode...")

    pairing_task = asyncio.create_task(led_pairing_pattern())
    service = aioble.Service(PAIR_UUID)

    rx_char = aioble.Characteristic(
        service, RX_UUID,
        write=True,
        write_no_response=True
    )

    tx_char = aioble.Characteristic(
        service, TX_UUID,
        notify=True
    )

    aioble.register_services(service)
    print("Waiting for BLE connection...")
    
    connection = await asyncio.wait_for(
        aioble.advertise(
            interval_us=20000,
            name=f"PicoW {get_pico_mac()}",
            services=[PAIR_UUID]
        ),
        timeout=180
    )

    pairing_task.cancel()
    print("BLE connected!")
    
    flash_task = asyncio.create_task(led_connected_flash())
    buffer = ""
    
    while True:
        print("Waiting for RX write...")

        # USE THE NEW EVENT API FOR RECEIVING WRITES
        await rx_char.written()
        raw = rx_char.read().decode()
        print("Received:", raw)
        
        try:
            new_cfg = ujson.loads(raw)
        except Exception as e:
            print("Invalid JSON:", e)
            continue

        save_config(new_cfg)
        print("Saved!")

        tx_char.write(b"OK")
        await tx_char.notify(connection)

        flash_task.cancel()
        reset()
