/*
*  This code is supporting material for the book
*  Python Programming for Arduino
*  by Pratik Desai
*  published by PACKT Publishing
*/

/*
Remote Home monitoring System
-----------------------------
Arduino based Monitoring station
Implements MQTT pubsub client for mosquitto broker hosted on Raspberry Pi based Control center
*/

#include <Wire.h>
#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
#include <SimpleTimer.h>

// Update these with values suitable for your network.
byte mac[]    = {  0x90, 0xA2, 0xDA, 0x0D, 0x3F, 0x62 };
byte server[] = { 10, 0, 0, 18 };
byte ip[]     = { 10, 0, 0, 75 };

#define GREEN 5
#define RED 3
#define BLUE 6
#define BUZZER 9
#define BUTTON 2
#define MotionPin 8
#define HumidityPin A0
#define LightPin A1

int partAddress = 0x48;

char message_buff[100];
char message_buff2[100];
char* temperatureC;
char* humidityC;
char* motionC;
char* lightC;

EthernetClient ethClient;
PubSubClient client(server, 1883, callback, ethClient);
SimpleTimer timer;

void callback(char* topic, byte* payload, unsigned int length) {
  // handle message arrived
  String topicS = String(topic);
  int i = 0;
  for(i=0; i<length; i++) {
    message_buff[i] = payload[i];
  }
  String payloadS = String(message_buff);
  memset(message_buff, 0, sizeof(message_buff));
  if(topicS == "MonitoringStation/led"){
    Serial.println(payloadS);
    if (payloadS.equals("red")){
      analogWrite(GREEN, 255);
      analogWrite(BLUE, 255);
      analogWrite(RED, 50);
      Serial.println("RED LED on");
    }
    else if (payloadS.equals("yellow")){
      analogWrite(RED, 50);
      analogWrite(BLUE, 255);
      analogWrite(GREEN, 50);
      Serial.println("YELLOW LED on");      
    }
    else if(payloadS.equals("green"))
    {
      analogWrite(GREEN, 50);
      analogWrite(RED, 255);
      analogWrite(BLUE, 255);
      Serial.println("GREEN LED on");
    }
    else{
      analogWrite(GREEN, 255);
      analogWrite(RED, 255);
      analogWrite(BLUE, 255);
    }
  }
  if(topicS.equals("MonitoringStation/buzzer")){
      if (payloadS=="ON"){
        Serial.println("Buzzer ON");
        digitalWrite(BUZZER, HIGH);
      }
      else{
        Serial.println("Buzzer OFF");
        digitalWrite(BUZZER, LOW);
      }
  }
  Serial.println();
}

void publishData (){
    Wire.requestFrom(partAddress,2);
    byte MSB = Wire.read();
    byte LSB = Wire.read();
    
    int TemperatureData = ((MSB << 8) | LSB) >> 4; 
  
    float celsius = TemperatureData*0.0625;
    temperatureC = dtostrf(celsius, 5, 2, message_buff2);
    client.publish("MonitoringStation/temperature", temperatureC);
    
    float humidity = getHumidity(celsius);
    humidityC = dtostrf(humidity, 5, 2, message_buff2);
    client.publish("MonitoringStation/humidity", humidityC);

    int motion = digitalRead(MotionPin);
    motionC = dtostrf(motion, 5, 2, message_buff2);
    client.publish("MonitoringStation/motion", motionC);
    
    int light = analogRead(LightPin);
    lightC = dtostrf(light, 5, 2, message_buff2);
    client.publish("MonitoringStation/light", lightC);
    Serial.println(lightC);
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

void buttonPress(){
    digitalWrite(BUZZER, LOW);
    Serial.println("Set buzzer off");
}

void setup()
{
  pinMode(GREEN, OUTPUT);
  pinMode(RED, OUTPUT);
  pinMode(BLUE, OUTPUT);
  analogWrite(GREEN, 255);
  analogWrite(RED, 255);
  analogWrite(BLUE, 255);
  pinMode(BUZZER, OUTPUT);
  pinMode(BUTTON, INPUT);
  pinMode(MotionPin, INPUT);
  Ethernet.begin(mac, ip);
  Serial.begin(9600);
  Wire.begin();
  if (client.connect("MonitoringStation")) {
    client.subscribe("MonitoringStation/led");
    client.subscribe("MonitoringStation/buzzer");
  }
  attachInterrupt(0, buttonPress, RISING);
  timer.setInterval(300000, publishData);
}

void loop()
{
  // Executing the timer
  timer.run();
  
  // Publishing keep alive message periodically, 
  // So the connection does not get expired from the broker side
  client.publish("MonitoringStation/alive", "y");
  client.loop();
}

  
