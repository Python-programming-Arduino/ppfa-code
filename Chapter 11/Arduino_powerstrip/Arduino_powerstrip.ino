/*
*  This code is supporting material for the book
*  Python Programming for Arduino
*  by Pratik Desai
*  published by PACKT Publishing
*/

/*
Tweet-a-Powerstrip
*/

#include <Wire.h>
#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.
byte mac[]    = {  0x90, 0xA2, 0xDA, 0x00, 0x47, 0x28 };
byte server[] = { 10, 0, 0, 20 };
byte ip[]     = { 10, 0, 0, 75 };

#define FAN 2
#define LAMP 3
#define TOASTER 6
#define COFFEEMAKER 9

char message_buff[100];
char reportChar[100];

boolean fanStatus;
boolean lampStatus;
boolean toasterStatus;
boolean coffeemakerStatus;

EthernetClient ethClient;
PubSubClient client(server, 1883, callback, ethClient);

void callback(char* topic, byte* payload, unsigned int length) {
  // handle message arrived
  String topicS = String(topic);
  int i = 0;
  // Create message string from payload
  for(i=0; i<length; i++) {
    message_buff[i] = payload[i];
  }
  String payloadS = String(message_buff);
  memset(message_buff, 0, sizeof(message_buff));
  Serial.println(topicS);
  Serial.println(payloadS);
  // Check topic with status and perform actions
  // Dealing with relay for fan
  if(topicS == "PowerStrip/fan"){
    if (payloadS.equalsIgnoreCase("on")) {
      digitalWrite(FAN, HIGH);
      fanStatus = true;
    }
    if (payloadS.equalsIgnoreCase("off")){
      digitalWrite(FAN, LOW);
      fanStatus = false;
    }
  }
  // Dealing with relay for lamp
  if(topicS == "PowerStrip/lamp"){
    if (payloadS.equalsIgnoreCase("on")) {
      digitalWrite(LAMP,HIGH);
      lampStatus = true;
    }
    if (payloadS.equalsIgnoreCase("off")){
      digitalWrite(LAMP,LOW);
      lampStatus = false;
    }
  }
  //Dealing with relay for toaster
  if(topicS == "PowerStrip/toaster"){
    if (payloadS.equalsIgnoreCase("on")) {
      digitalWrite(TOASTER, HIGH);
      toasterStatus = true;
    }
    if (payloadS.equalsIgnoreCase("off")){
      digitalWrite(TOASTER, LOW);
      toasterStatus = false;
    }
  }
  //Dealing with relay for coffee maker
  if(topicS == "PowerStrip/coffeemaker"){
    if (payloadS.equalsIgnoreCase("on")) {
      digitalWrite(COFFEEMAKER, HIGH);
      coffeemakerStatus = true;
    }
    if (payloadS.equalsIgnoreCase("off")){
      digitalWrite(COFFEEMAKER, LOW);
      coffeemakerStatus = false;
    } 
  } 
  if(topicS.equals("PowerStrip/statuscheck")){
    if (payloadS.equalsIgnoreCase("get")) {
        String report = "";
        if (fanStatus) report += "Fan:on,";
        else report += "Fan:off,";
   
        if (lampStatus) report += "Lamp:on,";
        else report += "Lamp:off,";
           
        if (toasterStatus) report += "Toaster:on,";
        else report += "Toaster:off,";
   
        if (coffeemakerStatus) report += "Coffeemaker:on";
        else report += "Coffeemaker:off";
      
        report.toCharArray(reportChar, 100);
        client.publish("PowerStrip/statusreport", reportChar);
    }
  }
  Serial.println();
}

void setup()
{
  pinMode(FAN, OUTPUT);
  pinMode(LAMP, OUTPUT);
  pinMode(TOASTER, OUTPUT);
  pinMode(COFFEEMAKER, OUTPUT);
  fanStatus = false;
  lampStatus = false;
  toasterStatus = false;
  coffeemakerStatus = false;
  digitalWrite(FAN, LOW);
  digitalWrite(LAMP,LOW);
  digitalWrite(TOASTER, LOW);
  digitalWrite(COFFEEMAKER, LOW);

  Ethernet.begin(mac, ip);
  Serial.begin(9600);
  Wire.begin();
  if (client.connect("PowerStrip")) {
    client.subscribe("PowerStrip/fan");
    client.subscribe("PowerStrip/lamp");
    client.subscribe("PowerStrip/toaster");
    client.subscribe("PowerStrip/coffeemaker");
    client.subscribe("PowerStrip/statuscheck");
  }
}

void loop()
{  
  /* Enable keep alive if face frequent disconnect
  *  Publishing keep alive message periodically, 
  *  So the connection does not get expired from the broker side
  */
  // client.publish("PowerStrip/alive", "y");
  
  client.loop();
}

  
