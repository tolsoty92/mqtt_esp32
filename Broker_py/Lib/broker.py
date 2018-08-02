#!python3
import paho.mqtt.client as mqtt  # import the client1
import time
from concurrent.futures import ThreadPoolExecutor

class Broker():

    def __init__(self, server_ip, port=1883):
        self.IP = server_ip
        self.broker_port = port
        mqtt.Client.connected_flag = False

    def wait_for(self, client, msgType, period=0.25):
        if msgType == "SUBACK":
            if client.on_subscribe:
                while not client.suback_flag:
                    print("waiting suback")
                    client.loop()  # check for messages
                    time.sleep(period)

    def initialize_clients(self, name, platforms):
        return {str(name) + '_' + str(i): mqtt.Client(str(name) + '_' + str(i))
                for i in platforms}

    def start_connection_client(self, client):
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        client.connect(self.IP, self.broker_port, keepalive=6)

    def on_connect(self, client, user_data, flags, rc):
        client.loop_start()
        if rc == 0:
            client.connected_flag = True  # set flag
            print("connected OK")
        else:
            print("Bad connection Returned code=", rc)

    def on_message(self, client, user_data, message):
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)
        print("message qos=", message.qos)
        print("message retain flag=", message.retain)

    def on_disconnect(self, client, user_rdata, rc=0):
        print("DisConnected result code " + str(rc))
        client.loop_stop()
        client.disconnect()