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
char humidityId[] = "HumidityRaw";
char pirId[] = "MotionRaw";

int ledPin = 2;
int pirPin = 3;

XivelyDatastream datastreamU[] = {
  XivelyDatastream(humidityId, strlen(humidityId), DATASTREAM_FLOAT),
  XivelyDatastream(pirId, strlen(pirId), DATASTREAM_FLOAT),
};
XivelyDatastream datastreamD[] = {
  XivelyDatastream(ledId, strlen(ledId), DATASTREAM_FLOAT),
};
// Finally, wrap the datastreams into a feed
XivelyFeed feedU(1649696305, datastreamU, 2 /* number of datastreams */);
XivelyFeed feedD(1649696305, datastreamD, 1 /* number of datastreams */);

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
  pinMode(pirPin, INPUT);
}

void loop() {
  // Downloading data from Xively
  int retD = xivelyclient.get(feedD, xivelyKey);
  Serial.print("xivelyclient.get returned ");
  Serial.println(retD);

  if (retD > 0)
  {
    Serial.println("Datastream is...");
    Serial.println(feedD[0]);

    Serial.print("LED value is: ");
    Serial.println(feedD[0].getFloat());
    
    if (feedD[0].getFloat() >= 1){
      digitalWrite(ledPin, HIGH);
    }
    else{
      digitalWrite(ledPin, LOW);
    }
  }
  Serial.println("LED status updated from xively channel value");
  Serial.println();
  
  // Uploading data to Xively
  int humidityValue = analogRead(A0);
  datastreamU[0].setFloat(humidityValue);
  int pirValue = digitalRead(pirPin);
  datastreamU[1].setFloat(pirValue);
  
  int retU = xivelyclient.put(feedU, xivelyKey);
  Serial.print("xivelyclient.put returned ");
  Serial.println(retU);
  Serial.println("Raw humidity and motion values sent to xively");
  Serial.println();
  delay(3000);
}

