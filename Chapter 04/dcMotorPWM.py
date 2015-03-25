#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

from pyfirmata import Arduino
from time import sleep
import os


# This function controls speed of the DC motor using PWM
def dcMotorControl(r, deltaT):
    pwmPin.write(r / 100.00)
    sleep(deltaT)
    pwmPin.write(0)


# Setting up the Arduino board
port = '/dev/cu.usbmodemfa1331'
board = Arduino(port)
# Need to give some time to pyFirmata and Arduino to synchronize
sleep(5)

# Set mode of pin 3 as PWM
pwmPin = board.get_pin('d:3:p')

# Testing the function by providing custom speed and time
try:
    while True:
        r = input("Enter value to set motor speed. (Between 1 to 100, 0 to exit): ")
        if (r > 100) or (r <= 0):
            print "Enter appropriate value."
            board.exit()
            break
        t = input("How long? (seconds)")
        dcMotorControl(r, t)
except KeyboardInterrupt:
    board.exit()
    os._exit()