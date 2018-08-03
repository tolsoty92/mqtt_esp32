from time import sleep
import paho.mqtt.client as mqtt  # import the client1
from concurrent.futures import ThreadPoolExecutor
from Client_py.Lib.func_module import  *

SERVER_IP = "192.168.0.121"
PORT = 1883
PLATFORMS_SET = {5,}
FEEDBACK_TOPIC = "esp32/feedback/+"
CONNECTON_TOPIC = "Connected"
MSG_TOPIC = "esp32/"

NUMBER_OF_CLIENTS = 1

MAX_WORKERS = 10
WORKER_TIME = 0.1
MESSAGES_QOS = 2

client = mqtt.Client("")

if __name__== "__main__":
    client = mqtt.Client("BOSS")
    pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    start_connection_client(client, SERVER_IP, PORT, CONNECTON_TOPIC)
    client.subscribe(FEEDBACK_TOPIC, qos=MESSAGES_QOS)
    while True:
        client.loop(WORKER_TIME)
        send_rand_msg(client, PLATFORM_SET, MSG_TOPIC, qos=MESSAGES_QOS)
        sleep(3)
        if not client.connected_flag:
            # if clients more than MAX_WORKERS, they add to pool and wait for reconnect
            f = pool.submit(client.loop, WORKER_TIME)