import network
import bluetooth
import time
import ntptime
from configuration import load_config
from pairing import pairing_mode
from scanner import BleScanner
import uasyncio as asyncio
from networking import WifiService
from machine import Pin, reset
from umqtt.simple import MQTTClient

def sync_time():
    try:
        ntptime.settime() 
        print(f"Time synced: {time.localtime()}")
    except Exception as e:
        print("NTP failed:", e)

def connect_mqtt(client_id, broker, port):
    mqtt_client = MQTTClient(
        client_id=client_id, 
        server=broker, 
        port=port)
    
    try:
        mqtt_client.connect()
        print("Connected to MQTT Broker")
        return mqtt_client
    
    except Exception as e:
        print("MQTT connection failed:", e)
        return False

async def main():
    try:
        config = load_config()
        pico_mac = WifiService.get_pico_mac()
        print(f'Pico MAC Address: {pico_mac}')
        
        if not config.get("wifi_ssid") or not config.get("wifi_password") or not config.get("mqtt_broker") or not config.get("mqtt_port"):
            await pairing_mode(config, pico_mac)
            
        if not WifiService.connect_wifi(config["wifi_ssid"],config["wifi_password"]):
            print("Could not connect to Wi-Fi, restarting...")
            time.sleep(5)
            reset()

        time.sleep(3)
        sync_time()
        
        mqtt_client = connect_mqtt(pico_mac, config["mqtt_broker"], config.get("mqtt_port", 30183))
        if not mqtt_client:
            print("MQTT not connected.")
            return
        
        ble = bluetooth.BLE()
        scanner = BleScanner(ble, mqtt_client, pico_mac)
        
        print("Starting BLE Scan...")
        while True:
            scanner.start_scan()
            time.sleep(2)
            
    except Exception as e:
        print("Error in main:", e)
        reset()
        
if __name__ == "__main__":
    asyncio.run(main())
