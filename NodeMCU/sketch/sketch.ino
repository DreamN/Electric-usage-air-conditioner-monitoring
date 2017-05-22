#include <ESP8266WiFi.h>
const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
void setup() 
{
    Serial.begin(115200);
    delay(10);
    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
   
    while (WiFi.status() != WL_CONNECTED)
    {
            delay(500);
            Serial.print(".");
    }
     
    IPAddress local_ip = {192,168,1,144};
    IPAddress gateway={192,168,1,1};
    IPAddress subnet={255,255,255,0};
    WiFi.config(local_ip,gateway,subnet);
 
    Serial.println(""); 
    Serial.println("WiFi connected");
    Serial.println("IP address: "); 
    Serial.println(WiFi.localIP());
}
void loop() {
}

