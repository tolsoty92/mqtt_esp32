#ifndef MqttClient 
#define MqttClient


#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <stdio.h>
#include <U8x8lib.h>

class mqttClient
{
    public:

        char* SSID;
        char* PASSWORD;
        char* MQTT_SERVER;
        String RECEIVED_DATA;
        bool MESSAGE_IS_REC = false;

        mqttClient(char* ssid, char* password, char* mqtt_server);
        void setup_wifi();
        void init_client_loop();
        void subscribe(int platform_id);
        void pub_msg(char* msg, int platform_id);
        void set_callback(void (*func)(char* topic, byte* message, unsigned int length));

};

#endif
