#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import time
from PyMata.pymata import PyMata

#Initializing Arduino using PyFirmata constructor
port = PyMata("COM5")

#Configure I2C pin
port.i2c_config(0, port.ANALOG, 4, 5)

# One shot read asking peripheral to send 2 bytes
port.i2c_read(0x23, 0, 2, port.I2C_READ)
# Wait for peripheral to send the data
time.sleep(3)

# Read from the peripheral
data = port.i2c_get_read_data(0x23)

# Obtain lux values from received data
LuxSum = (data[1] << 8 | data[2]) >> 4

lux = LuxSum/1.2
print str(lux) + ' lux'

port.close()
