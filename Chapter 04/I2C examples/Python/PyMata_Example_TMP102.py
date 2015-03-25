#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import time
from PyMata.pymata import PyMata

#Initialize Arduino using port name
port = PyMata("COM5")

#Configure I2C pin
port.i2c_config(0, port.ANALOG, 4, 5)

# One shot read asking peripheral to send 2 bytes
port.i2c_read(0x48, 0, 2, port.I2C_READ)
# Wait for peripheral to send the data
time.sleep(3)

# Read from the peripheral
data = port.i2c_get_read_data(0x48)

# Obtain temperature from received data
TemperatureSum = (data[1] << 8 | data[2]) >> 4

celsius = TemperatureSum * 0.0625
print celsius

fahrenheit = (1.8 * celsius) + 32
print fahrenheit

port.close()
