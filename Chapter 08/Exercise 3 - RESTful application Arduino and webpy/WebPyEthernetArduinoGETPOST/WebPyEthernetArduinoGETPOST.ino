#include <Ethernet.h>
#include <SPI.h>

EthernetClient client;
char serverName[] = "10.0.0.20";
//Setup
void setup() {
  Serial.begin(9600);
  // Connect via DHCP
  Serial.println("connect to network");
  //client.dhcp();

  // Can still fall back to manual config:
  byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x3F, 0x62 };
  //the IP address for the shield:
  byte ip[] = { 10, 0, 0, 75 };
  Ethernet.begin(mac,ip);
  Serial.println("Setup!");
}

String getResponse;
void loop(){
    if (client.connect(serverName, 8080)>0) {
      Serial.print("connected... ");
      Serial.println();
      client.println("GET /data HTTP/1.0");
      client.println();
    } else {
      Serial.println("connection failed");
    }
     if (client.connected()) {
        if (client.find("Humidity")){
            String data;
            data+="";
            data+="Humidity ";
            data+=analogRead(0);
            client.stop();
           if (client.connect("10.0.0.20",8080)) {
              Serial.println("connected");
              client.println("POST /data HTTP/1.1");
              client.println("Host: 10.0.0.20");
              client.println("Content-Type: application/x-www-form-urlencoded;");
              client.println("Connection: close");
              client.print("Content-Length: ");
              client.println(data.length());
              client.println();
              client.print(data);
              client.println();
              Serial.println("Humidity sent");
              client.stop();
          }
        }
        else{
            String data;
            data+="";
            data+="Motion ";
            data+=analogRead(1);
            client.stop();
           if (client.connect("10.0.0.20",8080)) {
              Serial.println("connected");
              client.println("POST /data HTTP/1.1");
              client.println("Host: 10.0.0.20");
              client.println("Content-Type: application/x-www-form-urlencoded;");
              client.println("Connection: close");
              client.print("Content-Length: ");
              client.println(data.length());
              client.println();
              client.print(data);
              client.println();
              Serial.println("Motion sent");
              client.stop();
          }
        }
     client.stop();
     delay(2000); 
  }
  delay(1000);
}
