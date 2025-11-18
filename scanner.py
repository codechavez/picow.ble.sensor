import uasyncio as asyncio
import ujson
import aioble
import bluetooth
import time
from mqtt_client import publish
from networking import get_pico_mac
from machine import Pin
from config import load_config

_IRQ_SCAN_RESULT = const(5)
CONFIGS = load_config()
led = Pin("LED", Pin.OUT)

class BleScanner:
    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)

    def blink_led(duration=0.1):
        led.on()
        time.sleep(duration)
        led.off()

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            qualifier = ''.join(['{:02X}'.format(b) for b in adv_data[13:23]])
            if qualifier == "DFFB48D2B060D0F5A710":
                self.dispatch_detection(addr_type, addr, rssi, adv_type, adv_data)
            
    def start_scan(self, duration_ms=5000):
        self._ble.gap_scan(0, duration_ms, 1000)

    def stop_scan(self):
        self._ble.gap_scan(None)

    def dispatch_detection(self, addr_type, addr, rssi, adv_type, adv_data):
        mac = ':'.join(['{:02X}'.format(b) for b in addr])
        print(f'Detected BLE - MAC: {mac}, RSSI: {rssi}')
        
        payload = ujson.dumps({
                "sensor": get_pico_mac(),
                "device": mac,
                "rssi": rssi,
                "timestamp": time.time(),
                "advertisementType": adv_type,
                "dataPayload": adv_data.hex() if adv_data else None,
            })
        
        led.on()
        publish(CONFIGS["mqtt_topic"], payload)
        led.off()
        print(f' Message sent to MQTT: {payload} ')