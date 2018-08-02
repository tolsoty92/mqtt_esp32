#include <MqttClient.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <stdio.h>
#include <U8x8lib.h>

char* ssid = "SPEECH_405";             // WiFi SSID
char* password = "multimodal";         // WiFi PASSWORD
char* mqtt_server = "192.168.0.121";   // Server ID
int platform_id = 5;                   // Platform ID

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


// Atantion! XXX is platform id

void setup()
{
    u8x8.begin();  // Init display
    u8x8.setFont(u8x8_font_chroma48medium8_r); // Set display's font
    u8x8.drawString(1,1,"Start setuping");     // Drawing string on display
    delay(2000);
    u8x8.clear();                              // Clear display
    mqtt.setup_wifi();                         // Connect to WiFi
    mqtt.set_callback(*callback);              // Set event for getting message in subscribed topic
    
    mqtt.pub_msg("Connected", platform_id);    // Send message "Connected" to topic <<esp32/feedback/XXX/>>
    u8x8.drawString(1,1,"End of setup");
    delay(2000);
    u8x8.clear();
}

void loop()
{                                              //if we lose the connection and reconnect then subscriptions will be renewed.
    mqtt.subscribe(platform_id);               // Subscribe on topic <<esp32/XXX/>>, where XXX is platform id. If cli
    mqtt.init_client_loop();                   // Init clien loop
    char msg[64] = "";                         // Init empty message variable
    RECEIVED_DATA.toCharArray(msg, 64);        // Pull text from RECEIVED_DATA to msg var
    RECEIVED_DATA = "";
    if (MESSAGE_IS_REC)                        // If we have a message on our topic
    {
        u8x8.drawString(1,1, msg);             // Draw msg
        mqtt.pub_msg(msg, platform_id);        // Send feedback msg to topic <<esp32/feedback/XXX/>>
        MESSAGE_IS_REC = false;
    }
    delay(1500);
    u8x8.clear();
}
