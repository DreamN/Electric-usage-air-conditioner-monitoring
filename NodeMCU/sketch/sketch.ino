#include <ESP8266WiFi.h>
#define SERVER_PORT 80

const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

const char* server_ip = "192.168.1.244";

String get_path = "GET /";
String param = " HTTP/1.1\r\n";
String server_host = "Host: 192.168.1.244\r\n\r\n";

WiFiServer server(SERVER_PORT);
WiFiClient client;

unsigned long previousMillis = 0;    
const long interval = 10000;

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

    // print data from server
    while(client.available())        
    {
          String line = client.readStringUntil('\n');
          Serial.println(line);
    }
    
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= interval)
    {
        previousMillis = currentMillis;
        Client_Request();
    }  
}
void Client_Request()
{
    Serial.println("Connect TCP Server");
    int cnt=0;
    while (!client.connect(server_ip,SERVER_PORT))
    {
          Serial.print(".");
          delay(100);
          cnt++;
          if(cnt>50)
          return;
    } 
    Serial.println("Success");
    delay(500);
    client.print(get_path+param+server_host);
    Serial.print(get_path+param+server_host);
    delay(100);
}
