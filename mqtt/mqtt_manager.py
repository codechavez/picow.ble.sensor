from umqtt.simple import MQTTClient

def mqtt_connect(cfg):
    try:
        client = MQTTClient(
            client_id="pico_ble",
            server=cfg["mqtt_host"],
            port=int(cfg["mqtt_port"])
        )
        client.connect()
        print("MQTT Connected")
        return client
    except Exception as e:
        print("MQTT failed:", e)
        return None
