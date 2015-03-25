/*
*  This code is supporting material for the book
*  Python Programming for Arduino
*  by Pratik Desai
*  published by PACKT Publishing
*/

/*
   Basic MQTT example
*
*  connects to an MQTT server
*  publishes "hello world" to the topic "outTopic"
*  subscribes to the topic "inTopic"
*/

#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.
byte mac[]    = {  0x90, 0xA2, 0xDA, 0x00, 0x47, 0x28 };
byte server[] = { 10, 0, 0, 20 };
byte ip[]     = { 10, 0, 0, 75 };

#define MotionPin 3
#define HumidityPin A0
char message_buff2[100];
char* humidityC;
char* motionC;

void callback(char* topic, byte* payload, unsigned int length) {
  // handle message arrived
}

EthernetClient ethClient;
PubSubClient client(server, 1883, callback, ethClient);

void setup()
{
  Ethernet.begin(mac, ip);
  Serial.begin(9600);
  if (client.connect("Arduino")) {
    client.publish("Arduino/connection","Connected.");
  }
}

void publishData()
{
  Serial.println("Publishing data...");
  float humidity = getHumidity(22.0);
  humidityC = dtostrf(humidity, 5, 2, message_buff2);
  client.publish("Arduino/humidity", humidityC);
  Serial.print("Arduino/humidity: ");
  Serial.println(humidityC);
  delay(5000);
  int motion = digitalRead(MotionPin);
  motionC = dtostrf(motion, 5, 2, message_buff2);
  client.publish("Arduino/motion", motionC);
  Serial.print("Arduino/motion: ");
  Serial.println(motionC);
  Serial.println("Data pbulished.");
}

float getHumidity(float degreesCelsius){
  //caculate relative humidity
  float supplyVolt = 5.0;

  // read the value from the sensor:
  int HIH4030_Value = analogRead(HumidityPin);
  float voltage = HIH4030_Value/1023. * supplyVolt; // convert to voltage value

  // convert the voltage to a relative humidity
  float sensorRH = 161.0 * voltage / supplyVolt - 25.8;
  float trueRH = sensorRH / (1.0546 - 0.0026 * degreesCelsius); //temperature adjustment 
  return trueRH;
}

void loop()
{
  publishData();
  delay(5000);
  client.loop();
}

