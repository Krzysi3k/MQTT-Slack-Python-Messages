from paho.mqtt import client as mqtt_client
import tele_mqtt_tasks
from datetime import datetime


broker = '192.168.0.123'
client_id = 'tele-python-docker-client'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe('tele/+/+')
    else:
        print(f"Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    received_msg = msg.payload.decode()
    try:
        _, device_name, func_name = msg.topic.split('/')
        obj_attr = getattr(tele_mqtt_tasks, func_name)
        func = obj_attr.get(device_name, None)
        if func is not None:
            # print(f'{datetime.now()} received msg on: {msg.topic}')
            func(device_name, received_msg)
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