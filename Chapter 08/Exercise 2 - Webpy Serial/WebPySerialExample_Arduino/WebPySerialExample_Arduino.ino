/*
*  This code is supporting material for the book
*  Python Programming for Arduino
*  by Pratik Desai
*  published by PACKT Publishing
*/

/*
 Arduino sketch to send HIH4030 raw sensor values to serial port.
 Web.py will use this data and display through the browser.
*/


void setup() {
  Serial.begin(9600);
}

void loop() {
  int analogChannel = 0;
  int HIH4030_Value = analogRead(analogChannel);
  Serial.println(HIH4030_Value);
  delay(200); 
}

