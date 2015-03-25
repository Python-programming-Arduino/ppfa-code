#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

from pyfirmata import Arduino, PWM
from time import sleep
import random

# Setting up the Arduino board
port = '/dev/cu.usbmodemfa1311'
board = Arduino(port)
# Need to give some time to pyFirmata and Arduino to synchronize
sleep(5)

# Setup mode of pin 2 as PWM
pin = 11
board.digital[pin].mode = PWM

for i in range(0, 99):
    # This python method generate random value between given range
    r = random.randint(1, 100)

    board.digital[pin].write(r / 100.00)
    # divide by 100.00 here as the answer will be float, integer otherwise
    sleep(0.1)

board.digital[pin].write(0)
board.exit()