from umqtt.simple import MQTTClient

client = None

def mqtt_connect(host, port, client_id):
    global client
    client = MQTTClient(client_id, host, port=port)
    client.connect()

def mqtt_publish(topic, msg):
    global client
    client.publish(topic, msg)
