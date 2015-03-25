/* This code is supporting material for the book
*  Python Programming for Arduino
*  by Pratik Desai
*  published by PACKT Publishing
*/

/*
* Thermostat sketch for Method 1
*
* TMP102 sensor for Temperature - I2C
* HIH4030 Humidity sensor - Analog pin
* BH1750 Ambient light sensor - I2C
* Push button - Digital in
*/

#include <Wire.h>
#include <BH1750.h>

int tmp102Address = 0x48;
int HIH4030_Pin = A0; //analog pin 0
BH1750 lightMeter;
boolean flagTemperature = false;
boolean flagPlot = false;

void setup(){
  Serial.begin(9600);
  lightMeter.begin();
  Wire.begin();
  attachInterrupt(0, button1Press, RISING);
  attachInterrupt(1, button2Press, RISING);
}

void loop(){
  
  uint16_t lux = lightMeter.readLightLevel();
  Serial.print("Light(lx):");
  Serial.println(lux);
  delay(200);
  
  float celsius = getTemperature();
  float fahrenheit = (1.8 * celsius) + 32;  
  if (flagTemperature == 1){
    Serial.print("Temperature(C):");
    Serial.println(celsius);
  } else {
    Serial.print("Temperature(F):");
    Serial.println(fahrenheit);
  }
  delay(200); 
  
  float relativeHumidity  = getHumidity(celsius);
  Serial.print("Humidity(%):");
  Serial.println(relativeHumidity);
  delay(200); 
  
  Serial.print("Flag:");
  Serial.println(flagPlot);
  delay(200);   
}

float getTemperature(){
  Wire.requestFrom(tmp102Address, 2); 

  byte MSB = Wire.read();
  byte LSB = Wire.read();

  //it's a 12bit int, using two's compliment for negative
  int TemperatureSum = ((MSB << 8) | LSB) >> 4; 

  float celsius = TemperatureSum*0.0625;
  return celsius;
}

float getHumidity(float degreesCelsius){
  //caculate relative humidity
  float supplyVolt = 5.0;

  // read the value from the sensor:
  int HIH4030_Value = analogRead(HIH4030_Pin);
  float voltage = HIH4030_Value/1023. * supplyVolt; // convert to voltage value

  // convert the voltage to a relative humidity
  // - the equation is derived from the HIH-4030/31 datasheet
  // - it is not calibrated to your individual sensor
  //  Table 2 of the sheet shows the may deviate from this line
  float sensorRH = 161.0 * voltage / supplyVolt - 25.8;
  float trueRH = sensorRH / (1.0546 - 0.0026 * degreesCelsius); //temperature adjustment 

  return trueRH;
}
void button1Press(){
  if (flagTemperature == 0){
    flagTemperature = 1;
  }
  else{
    flagTemperature = 0;
  }
}

void button2Press(){
  if (flagPlot == 0){
    flagPlot = 1;
  }
  else{
    flagPlot = 0;
  }
}
