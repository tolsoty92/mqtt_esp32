#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <stdio.h>
#include <U8x8lib.h>
#include <MqttClient.h>


WiFiClient espClient;
PubSubClient* client;


mqttClient::mqttClient(char* ssid, char* password, char* mqtt_server)
{
    SSID = ssid;
    PASSWORD = password;
    client = new PubSubClient(espClient);
    client->setServer(mqtt_server, 1883);
}


void mqttClient::setup_wifi()
{
    WiFi.begin(SSID, PASSWORD);    
    delay(500);
    while (WiFi.status() != WL_CONNECTED) 
    {
        delay(1000);
    }    
}

void mqttClient::init_client_loop()
{
    client->loop();
}

void mqttClient::subscribe(int platform_id)
{
    char topic[64];
    sprintf(topic, "esp32/%d/", platform_id);
    //Loop until we're reconnected
    while (!client->connected()) {
        // Attempt to connect
        if (client->connect("ESP8266Client")) {
        // Subscribe to topic
        client->subscribe(topic);
        } else {
        // Wait 0.5 seconds before retrying
        delay(500);
        }
    }
}

void mqttClient::pub_msg(char* msg, int platform_id)
{
    char theme[64];
    char topic[64];
    sprintf(topic, "esp32/feedback/%d/", platform_id);
    sprintf(theme, "Message <<%s>> is received!",msg);
    client->publish(topic, theme);
}

// void callback(char* topic, byte* message, unsigned int length)
// {   
//     // 
//     // for (int i = 0; i < length; i++) {
//     //     RECEIVED_DATA += (char)message[i];
//     // } 
//     // MESSAGE_IS_REC = true;
// }

void mqttClient::set_callback(void (*callback)(char* topic, byte* message, unsigned int length))
{
    client->setCallback(callback);
}