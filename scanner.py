import uasyncio as asyncio
import ujson
import aioble
import bluetooth
import time
from datetime import datetime
from machine import Pin
from configuration import load_config

_IRQ_SCAN_RESULT = const(5)
CONFIGS = load_config()
led = Pin("LED", Pin.OUT)
    
class BleScanner:
    def __init__(self, ble, mqtt, mac_address):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._mqtt = mqtt
        self._mac_address = mac_address

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            
            qualifier = ''.join(['{:02X}'.format(b) for b in adv_data[13:23]])
            if qualifier == "DFFB48D2B060D0F5A710":
                self.dispatch_detection(addr_type, addr, rssi, adv_type, adv_data)

    def start_scan(self, duration_ms=5000):
        self._ble.gap_scan(0, duration_ms, 2000)

    def stop_scan(self):
        self._ble.gap_scan(None)

    def dispatch_detection(self, addr_type, addr, rssi, adv_type, adv_data):
        mac = ':'.join(['{:02X}'.format(b) for b in addr])
        print(f'Detected BLE - MAC: {mac}, RSSI: {rssi}')
        
        now_utc = time.time() 
        payload = ujson.dumps({
                "sensor": self._mac_address,
                "device": mac,
                "rssi": rssi,
                "timestamp": now_utc,
                "advertisementType": adv_type,
                "dataPayload": adv_data.hex() if adv_data else None,
            })
        
        led.on()
        self._mqtt.publish(CONFIGS["mqtt_topic"], payload)
        led.off()
        print(f' Message sent to MQTT: {payload} ')