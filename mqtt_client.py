from umqtt.simple import MQTTClient

mqtt_client = None

def connect_mqtt(client_id, broker, port=1883):
    global mqtt_client
    mqtt_client = MQTTClient(client_id=client_id, server=broker, port=port)
    try:
        mqtt_client.connect()
        print("MQTT connected")
        return True
    except Exception as e:
        print("MQTT connection failed:", e)
        return False

def publish(topic, message):
    try:
        mqtt_client.publish(topic, message)
        
    except Exception as e:
        print("MQTT publish failed:", e)