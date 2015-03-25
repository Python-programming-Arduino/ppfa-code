/*
*  This code is supporting material for the book
*  Python Programming for Arduino
*  by Pratik Desai
*  published by PACKT Publishing
*/

#include <Ethernet.h>
#include <SPI.h>

byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0x47, 0x28 };
//the IP address for the shield:
byte ip[] = { 10, 0, 0, 75 };
EthernetClient client;
int analogChannel = 0;
void setup()
{
  Serial.begin(9600);
  Ethernet.begin(mac);
  delay(1000);
  Serial.println("connecting...");
}

void loop(){
  String data;
  data+="";
  data+="Humidity ";
  data+=analogRead(analogChannel);
  
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
    
    Serial.println("Data sent.");
  }
  delay(2000);
  
  if (client.connected()) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
  }
}

