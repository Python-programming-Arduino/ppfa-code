#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

from pyfirmata import Arduino
from pyfirmata import SERVO
from time import sleep

# Setting up the Arduino board
port = 'COM5'
board = Arduino(port)
# Need to give some time to pyFirmata and Arduino to synchronize
sleep(5)

# Set mode of the pin 13 as SERVO
pin = 13
board.digital[pin].mode = SERVO


# Custom angle to set Servo motor angle
def setServoAngle(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)

# Testing the function by rotating motor in both direction
while True:
    for i in range(0, 180):
        setServoAngle(pin, i)
    for i in range(180, 1, -1):
        setServoAngle(pin, i)

    # Continue or break the testing process
    i = raw_input("Enter 'y' to continue or Enter to quit): ")
    if i == 'y':
        pass
    else:
        board.exit()
        break