#include <MqttClient.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <stdio.h>


char* ssid = "SPEECH_405";
char* password = "multimodal";
char* mqtt_server = "192.168.0.121";
int platform_id = 5;

String RECEIVED_DATA;
bool MESSAGE_IS_REC = false;

mqttClient mqtt(ssid, password, mqtt_server);

void callback(char* topic, byte* message, unsigned int length)
{
    for (int i = 0; i < length; i++)
    {
        RECEIVED_DATA += (char)message[i];
    }
    MESSAGE_IS_REC = true;
}


void setup()
{
    delay(2000);
    mqtt.setup_wifi();
    mqtt.set_callback(*callback);
    delay(2000);
}

void loop()
{
    mqtt.subscribe(platform_id);
    mqtt.init_client_loop();
    char msg[64] = "";
    RECEIVED_DATA.toCharArray(msg, 64);
    RECEIVED_DATA = "";
    if (MESSAGE_IS_REC)
    {
        mqtt.pub_feedback(msg, platform_id);
        MESSAGE_IS_REC = false;
    }
    delay(10);
}