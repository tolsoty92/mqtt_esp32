from concurrent.futures import ThreadPoolExecutor
from Broker_py.Lib.broker import Broker
import time



BROKER_IP = "192.168.0.121"
BROKER_PORT = 1883
PLATFORM_ID = [5]
NUMBER_OF_CLIENTS = 1

MAX_WORKERS = 10
WORKER_TIME = 0.1
MESSAGES_QOS = 5

PLATFORM_TOPICS = []
for id in PLATFORM_ID:
    PLATFORM_TOPICS.append("esp32/%d/" % id)

if __name__ == "__main__":
    broker = Broker(BROKER_IP, BROKER_PORT)
    pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    clients = broker.initialize_clients("Platform", PLATFORM_ID)
    print(clients)


    for key, client in clients.items():
        broker.start_connection_client(client)
        for id in PLATFORM_ID:
            feedback_topic = "esp32/feedback/" + str(id) +"/"
            client.subscribe(feedback_topic, 2)

    while True:
        for key, client in clients.items():
            client.loop(WORKER_TIME)
            id = input("Chose platform ID: ")
            topic = "esp32/" + str(id) +"/"
            msg = input("Wrie message: ")
            client.publish(topic,msg, 2)
            time.sleep(1)
            if not client.connected_flag:
                # if clients more than MAX_WORKERS, they add to pool and wait for reconnect
                f = pool.submit(client.loop, WORKER_TIME)