import aioble
import bluetooth
import ujson
from config import save_config
from networking import get_pico_mac

PAIR_UUID = aioble.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
RX_UUID   = aioble.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
TX_UUID   = aioble.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

async def run_ble_pairing():
    ble = bluetooth.BLE()
    ble.active(True)

    service = aioble.Service(PAIR_UUID)
    rx_char = aioble.Characteristic(service, RX_UUID, write=True)
    tx_char = aioble.Characteristic(service, TX_UUID, notify=True)
    aioble.register_services(service)

    pico_mac = get_pico_mac()

    adv = aioble.advertise(
        100000,
        name="PICO_PAIR",
        services=[PAIR_UUID],
    )

    print("Waiting for phone...")
    connection = await aioble.accept()

    # Send Pico MAC identity
    identity = {
        "device_mac": pico_mac,
        "device_type": "pico_w",
        "mode": "pairing"
    }
    await tx_char.notify(ujson.dumps(identity))

    # Wait for credentials
    data = await rx_char.written()
    payload = ujson.loads(bytes(data).decode())

    # Persist configuration
    save_config(payload)

    # Confirmation
    resp = {
        "status": "ok",
        "device_mac": pico_mac
    }
    await tx_char.notify(ujson.dumps(resp))

    await connection.disconnect()
