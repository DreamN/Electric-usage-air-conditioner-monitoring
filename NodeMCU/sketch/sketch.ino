#include <ESP8266WiFi.h>
#define SERVER_PORT 8080

const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

const char* server_ip = "192.168.1.244";

String get_path = "POST /updatestatus";
String param = " HTTP/1.1\r\n";
String server_host = "Host: 192.168.1.244\r\n\r\n";

String room_id = "1";
int state = 0;
int state_a = 0;

String myURL(String n_status, String a_status){
    String new_path = get_path + "?id=" + room_id + "&status=" + n_status + "&aircon=" + a_status + param + server_host;
    return new_path;
}

WiFiServer server(SERVER_PORT);
WiFiClient client;

unsigned long previousMillis = 0;    
const long interval = 10000;

void setup() 
{
    pinMode(D3, OUTPUT);
    pinMode(D4, INPUT);
    pinMode(D7, OUTPUT);
    pinMode(D8, INPUT);
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

    int read_s_val = digitalRead(D8);
    int read_a_val = digitalRead(D4);
    
    if(read_s_val != state){
      state = read_s_val;
      if(read_s_val == 1){
        Serial.println("SWITCH ON");
        digitalWrite(D7, HIGH);
        digitalWrite(D3, state_a);
      }
      else{
        Serial.println("SWITCH OFF"); 
        digitalWrite(D7, LOW);
        digitalWrite(D3, LOW);
      }
      Client_Request(read_s_val, state_a);
    }
    if(read_a_val != state_a){
      state_a = read_a_val;
      if(read_a_val == 1){ 
        digitalWrite(D3, state);
        if(state == 1){
          Serial.println("AIRCON ON");
          Client_Request(read_s_val, state_a);
        }
        else{ 
          Serial.println("CANNOT TURN AIRCON ON/OFF (ON)");
        }
      }
      else{
        digitalWrite(D3, LOW);
        if(state == 1){
          Serial.println("AIRCON OFF");
          Client_Request(read_s_val, state_a);
        }
        else{ 
          Serial.println("CANNOT TURN AIRCON ON/OFF (OFF)");
        }
      } 
    }
    delay(2000);
}
void Client_Request(int status_led, int status_aircon)
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
      if(status_aircon == 1){
        client.print(myURL("ON", "ON"));
        Serial.print(myURL("ON", "ON"));
      }
      else{
        client.print(myURL("ON", "OFF"));
        Serial.print(myURL("ON", "OFF"));  
      }
    }
    else{
      client.print(myURL("OFF", "OFF"));
      Serial.print(myURL("OFF", "OFF"));
    }
    delay(100);
}