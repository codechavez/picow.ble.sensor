import network
import time
import bluetooth
import uasyncio as asyncio
from config import load_config
from pairing import pairing_mode
from scanner import BleScanner
from umqtt.simple import MQTTClient
import ntptime

def connect_mqtt(client_id, broker, port):
    mqtt_client = MQTTClient(
        client_id=client_id, 
        server=broker, 
        port=port)
    
    try:
        mqtt_client.connect()
        print("MQTT connected")
        return mqtt_client
    
    except Exception as e:
        print("MQTT connection failed:", e)
        return False
    
wlan = network.WLAN(network.STA_IF)
def connect_wifi(ssid, password):
    wlan.active(True)
    wlan.connect(ssid, password)
    for _ in range(20):
        if wlan.isconnected():
            ip, subnet, gateway, dns = wlan.ifconfig()
            print(f"Connected to Wi-Fi with IP Address: {ip}")
            sync_time()
            return True
        time.sleep(1)
    print("Wi-Fi connection failed")
    return False

def get_pico_mac():
    wlan.active(True)
    mac = wlan.config("mac")
    return ':'.join('{:02X}'.format(b) for b in mac)

def sync_time():
    try:
        ntptime.settime() 
        print("Time synced")
    except Exception as e:
        print("NTP failed:", e)

async def main():
    config = load_config()
    pico_mac = get_pico_mac()
    print(f'Pico MAC Address: {pico_mac}')
    
    if not config.get("wifi_ssid") or not config.get("wifi_password") or not config.get("mqtt_broker") or not config.get("mqtt_port"):
        await pairing_mode(config)
    
    connect_wifi(config["wifi_ssid"], config["wifi_password"])
    mqtt_client = connect_mqtt(pico_mac, config["mqtt_broker"], config.get("mqtt_port", 30183))
    if not mqtt_client:
        print("MQTT not connected.")
        return
    
    time.sleep(3)
    
    ble = bluetooth.BLE()
    scanner = BleScanner(ble, mqtt_client)
    
    print("Starting BLE scan...")
    while True:
        scanner.start_scan()
        time.sleep(2)
        
if __name__ == "__main__":
    asyncio.run(main())
    