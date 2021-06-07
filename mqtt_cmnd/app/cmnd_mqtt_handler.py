from paho.mqtt import client as mqtt_client
import cmnd_mqtt_tasks


broker = '192.168.0.123'
client_id = 'cmnd-python-docker-client'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe('cmnd/+/+')
    else:
        print(f"Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    received_msg = msg.payload.decode()
    # print(f"received msg: {received_msg} on topic: {msg.topic}")
    try:
        _, hostname, func_name = msg.topic.split('/')
        func = getattr(cmnd_mqtt_tasks, func_name)
        func(hostname, received_msg)
    except Exception as e:
        pass


def make_client():
    client = mqtt_client.Client(client_id)
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(broker, port=1883)
    return client


if __name__ == "__main__":
    client = make_client()
    client.loop_forever()