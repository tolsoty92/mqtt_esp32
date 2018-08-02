#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <stdio.h>
#include <U8x8lib.h>


class mqtt_client
{
    public:

    char* SSID;
    char* PASSWORD;
    char* MQTT_SERVER;

    int PLATFORM_ID;
    static String RECEIVED_DATA;
    static long last_msg;
    //char* TOPIC;
    
    WiFiClient espClient;
    PubSubClient* client;


    mqtt_client(char* ssid, char* password, char* mqtt_server, int platform_id)
    {
        SSID = ssid;
        PASSWORD = password;
        PLATFORM_ID = platform_id;
        client = new PubSubClient(espClient);
        client -> setServer(mqtt_server, 1883);
    }



    void setup_wifi()
    {
        WiFi.begin(SSID, PASSWORD);        
    }


    void init_client_loop()
    {
        client->loop();
    }


    void subscribe(int platform_id)
    {
        char topic[32];
        sprintf(topic, "esp32/%d/", platform_id);
        //Loop until we're reconnected
        while (!client->connected()) {
            // Attempt to connect
            if (client->connect("ESP8266Client")) {
            Serial.println("connected");
            // Subscribe to topic
            client->subscribe(topic);
            } else {
            // Wait 5 seconds before retrying
            delay(5000);
            }
        }
    }


    void pub_msg(char* msg, int platform_id)
    {
        char theme[64];
        char topic[64];
        sprintf(topic, "esp32/feedback/%d/", platform_id);
        sprintf(theme, "Message <<%s>> is received!",msg);
        client->publish(topic, theme);
    }

};



char* ssid = "SPEECH_405";
char* password = "multimodal";
char* mqtt_server = "192.168.0.121";
int platform_id = 5;

String RECEIVED_DATA;
bool MESSAGE_IS_REC = false;

mqtt_client mqtt(ssid, password, mqtt_server, platform_id);
U8X8_SSD1306_128X64_NONAME_SW_I2C u8x8(15,4,16);


void callback(char* topic, byte* message, unsigned int length)
{   
    for (int i = 0; i < length; i++) {
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
    mqtt.client->setCallback(callback);
    mqtt.subscribe(platform_id);
    mqtt.pub_msg("Connected", platform_id);
    u8x8.drawString(1,1,"End of setup");
    delay(2000);
}

void loop()
{
    mqtt.init_client_loop();    
    char msg[64] = "";
    RECEIVED_DATA.toCharArray(msg, 64);
    RECEIVED_DATA = "";
    u8x8.drawString(1,1, msg);
    if (MESSAGE_IS_REC)
    {
      mqtt.pub_msg(msg, platform_id);
      MESSAGE_IS_REC = false;
    }

    delay(1500);
    u8x8.clear();
}
