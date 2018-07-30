#!python3
import paho.mqtt.client as mqtt  # import the client1
import time
from concurrent.futures import ThreadPoolExecutor

BROKER_IP = "192.168.0.121"
BROKER_PORT = 1883
NAME_OF_CLIENTS = "test_ID"
NUMBER_OF_CLIENTS = 1

MAX_WORKERS = 10
WORKER_TIME = 0.1
MESSAGES_QOS = 5

TOPICS = {'temperature': "esp32/temperature", 'humidity': "esp32/humidity"}
mqtt.Client.connected_flag = False  # create flag in class


def wait_for(client, msgType, period=0.25):
    if msgType == "SUBACK":
        if client.on_subscribe:
            while not client.suback_flag:
                print("waiting suback")
                client.loop()  # check for messages
                time.sleep(period)


def initialize_clients(name, number):
    return {str(name) + '_' + str(i): mqtt.Client(str(name) + '_' + str(i))
            for i in range(0, number)}


def start_connection_client(client, broker, port):
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, port, keepalive=6)


def on_connect(client, user_data, flags, rc):
    client.loop_start()
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_message(client, user_data, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def on_disconnect(client, user_rdata, rc=0):
    print("DisConnected result code " + str(rc))
    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":

    pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    clients = initialize_clients(NAME_OF_CLIENTS, NUMBER_OF_CLIENTS)
    print(clients)

    for key, client in clients.items():
        start_connection_client(client, BROKER_IP, BROKER_PORT)
        client.subscribe([(TOPICS['temperature'], 0), (TOPICS['humidity'], 0)])

    while True:
        for key, client in clients.items():
            client.loop(WORKER_TIME)
            client.publish("esp32/temperature","temperature")
            client.publish("esp32/humidity", "humidity")
            time.sleep(0.5)
            if not client.connected_flag:
                # if clients more than MAX_WORKERS, they add to pool and wait for reconnect
                f = pool.submit(client.loop, WORKER_TIME)