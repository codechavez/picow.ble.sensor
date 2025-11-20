import aioble
import time
import ujson
import uasyncio as asyncio
from machine import Pin, reset
from bluetooth import UUID
from configuration import save_config

PAIR_UUID = UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
RX_UUID   = UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
TX_UUID   = UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

led = Pin("LED", Pin.OUT)
PAIRING_TIMEPOUT = 180

REQUIRED_FIELDS = ["wifi_ssid", "wifi_password", "mqtt_broker", "mqtt_port", "mqtt_topic"]

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
async def pairing_mode(config, mac_address):
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
            name=f"PicoW {mac_address}",
            services=[PAIR_UUID]
        ),
        timeout=180
    )

    pairing_task.cancel()
    print("BLE connected!")
    
    flash_task = asyncio.create_task(led_connected_flash())
    buffer = ""
    
    while True:
        try:
            await rx_char.written()
            chunk = rx_char.read()
            if not chunk:
                continue
            
            print("Chunk received:", chunk)
            buffer += chunk.decode()
            
            try:
                data = ujson.loads(buffer)
                print("Data received:", data)
            except ValueError:
                continue
            
            # Validate required fields
            missing = [k for k in REQUIRED_FIELDS if k not in data or not data[k]]
            if missing:
                print("Missing fields:", missing)
                tx_char.write(b"ERR: Missing required fields")
                continue 
            
            # SAVE YOUR CONFIG HERE
            save_config(data)
            print("Configuration saved, restarting...")
            tx_char.write(b"OK")
            flash_task.cancel()
            time.sleep(1)
            reset()
            
        except Exception as e:
            flash_task.cancel()
            time.sleep(1)
            reset()