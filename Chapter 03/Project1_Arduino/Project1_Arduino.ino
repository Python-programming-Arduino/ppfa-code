/* This code is supporting material for the book
*  Python Programming for Arduino
*  by Pratik Desai
*  published by PACKT Publishing
*/

int pirPin = 8; //Pin number for PIR sensor
int redLedPin = 12; //Pin number for Red LED
int greenLedPin = 13; //Pin number for Green LED

void setup(){
 Serial.begin(9600); 
 pinMode(pirPin, INPUT);
 pinMode(redLedPin, OUTPUT);
 pinMode(greenLedPin, OUTPUT);
}
void loop(){
  int pirVal = digitalRead(pirPin);
  if(pirVal == LOW){ //was motion detected
    blinkLED(greenLedPin, "No motion detected.");
  } else {
    blinkLED(redLedPin, "Motion detected.");
  }
}
// Function which blinks LED at specified pin number
void blinkLED(int pin, String message){
  digitalWrite(pin,HIGH);
  Serial.println(message); 
  delay(1000);
  digitalWrite(pin,LOW);
  delay(2000);
}
