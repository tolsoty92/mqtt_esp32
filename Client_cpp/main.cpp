#include <MqttClient.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <stdio.h>
#include <U8x8lib.h>

char* ssid = "SPEECH_405";
char* password = "multimodal";
char* mqtt_server = "192.168.0.121";
int platform_id = 5;

String RECEIVED_DATA;
bool MESSAGE_IS_REC = false;

mqttClient mqtt(ssid, password, mqtt_server);
U8X8_SSD1306_128X64_NONAME_SW_I2C u8x8(15,4,16);


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
    u8x8.begin();
    u8x8.setFont(u8x8_font_chroma48medium8_r);
    u8x8.drawString(1,1,"Start setuping");
    delay(2000);
    u8x8.clear();
    mqtt.setup_wifi();
    mqtt.set_callback(*callback);
    mqtt.subscribe(platform_id);
    mqtt.pub_msg("Connected", platform_id);
    u8x8.drawString(1,1,"End of setup");
    delay(2000);
    u8x8.clear();
}

void loop()
{
    mqtt.init_client_loop();    
    char msg[64] = "";
    RECEIVED_DATA.toCharArray(msg, 64);
    RECEIVED_DATA = "";
    if (MESSAGE_IS_REC)
    {
        u8x8.drawString(1,1, msg);
        mqtt.pub_msg(msg, platform_id);
        MESSAGE_IS_REC = false;
    }
    delay(1500);
    u8x8.clear();
}
