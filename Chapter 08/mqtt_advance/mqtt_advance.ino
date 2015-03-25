/*
*  This code is supporting material for the book
*  Python Programming for Arduino
*  by Pratik Desai
*  published by PACKT Publishing
*/

#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.
byte mac[]    = {  0x90, 0xA2, 0xDA, 0x00, 0x47, 0x28 };
byte server[] = { 10, 0, 0, 20 };
byte ip[]     = { 10, 0, 0, 75 };

void callback(char* topic, byte* payload, unsigned int length) {
  // handle message arrived
  Serial.print(topic);
  Serial.print(':');
  Serial.write(payload,length);
  Serial.println();
}

EthernetClient ethClient;
PubSubClient client(server, 1883, callback, ethClient);

void setup()
{
  Serial.begin(9600);
  Ethernet.begin(mac, ip);
  if (client.connect("arduinoClient")) {
    client.subscribe("inTopic");
  }
}

void loop()
{
  client.publish("outTopic","From Arduino");
  delay(1000);
  client.loop();
}

