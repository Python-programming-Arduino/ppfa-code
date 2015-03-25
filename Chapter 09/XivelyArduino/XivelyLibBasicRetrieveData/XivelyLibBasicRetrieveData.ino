/*
*  This code is supporting material for the book
*  Python Programming for Arduino
*  by Pratik Desai
*  published by PACKT Publishing
*/

#include <SPI.h>
#include <Ethernet.h>
#include <HttpClient.h>
#include <Xively.h>

// MAC address for your Ethernet shield
// MAC address for your Ethernet shield
byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x3F, 0x62 };

// Your Xively key to let you upload data
char xivelyKey[] = "OKJacI8hWH46jiDKh6oodaJQWatpdPEELl0Nm25UOG5GxSFY";

// Define the string for our datastream ID
char ledId[] = "LED";
int ledPin = 2;

XivelyDatastream datastreams[] = {
  XivelyDatastream(ledId, strlen(ledId), DATASTREAM_FLOAT),
};
// Finally, wrap the datastreams into a feed
XivelyFeed feed(1649696305, datastreams, 1 /* number of datastreams */);

EthernetClient client;
XivelyClient xivelyclient(client);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  Serial.println("Reading from Xively example");
  Serial.println();

  while (Ethernet.begin(mac) != 1)
  {
    Serial.println("Error getting IP address via DHCP, trying again...");
    delay(15000);
  }
  // Setting up LED pin
  pinMode(ledPin, OUTPUT);
}

void loop() {
  int ret = xivelyclient.get(feed, xivelyKey);
  Serial.print("xivelyclient.get returned ");
  Serial.println(ret);

  if (ret > 0)
  {
    Serial.println("Datastream is...");
    Serial.println(feed[0]);

    Serial.print("LED value is: ");
    Serial.println(feed[0].getFloat());
    
    if (feed[0].getFloat() >= 1){
      digitalWrite(ledPin, HIGH);
    }
    else{
      digitalWrite(ledPin, LOW);
    }
  }

  Serial.println();
  delay(3000);
}

