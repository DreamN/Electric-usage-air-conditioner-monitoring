#include <ESP8266WiFi.h>
#define SERVER_PORT 80

const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

const char* server_ip = "192.168.1.244";

String get_path = "POST /updatestatus";
String param = " HTTP/1.1\r\n";
String server_host = "Host: 192.168.1.244\r\n\r\n";

String room_id = "1";
int state = 1;

String myURL(String n_status){
    String new_path = get_path + "?id=\"" + room_id + "\"&status=\"" + n_status + "\"" + param + server_host;
    return new_path;
}

WiFiServer server(SERVER_PORT);
WiFiClient client;

unsigned long previousMillis = 0;    
const long interval = 10000;

void setup() 
{
    pinMode(D8, INPUT);
    pinMode(D7, OUTPUT);
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

    Serial.println("Read Value"); 
    int read_val = digitalRead(D8);
    
    unsigned long currentMillis = millis();
    if(read_val != state){
      state = read_val;
      if(read_val == 1){
        Serial.println("SWITCH ON");
        digitalWrite(D7, HIGH);
      }
      else{
        Serial.println("SWITCH OFF"); 
        digitalWrite(D7, LOW);
      }
      Client_Request(read_val);
    }
    delay(2000);
}
void Client_Request(int status_led)
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
    if(status_led==1){
      client.print(myURL("ON"));
      Serial.print(myURL("ON"));
    }
    else{
      client.print(myURL("OFF"));
      Serial.print(myURL("OFF"));
    }
    delay(100);
}