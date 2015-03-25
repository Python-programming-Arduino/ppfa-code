/* This code is supporting material for the book
*  Python Programming for Arduino
*  by Pratik Desai
*  published by PACKT Publishing
*/

#include <Wire.h>
int partAddress = 0x48;

void setup(){
  Serial.begin(9600);
  Wire.begin();
}

void loop(){

  Wire.requestFrom(partAddress,2);
  byte MSB = Wire.read();
  byte LSB = Wire.read();

  int TemperatureData = ((MSB << 8) | LSB) >> 4; 

  float celsius = TemperatureData*0.0625;
  Serial.print("Celsius: ");
  Serial.println(celsius);

  float fahrenheit = (1.8 * celsius) + 32;  
  Serial.print("Fahrenheit: ");
  Serial.println(fahrenheit);

  delay(500); 
}
