#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

from pyfirmata import Arduino, util
from time import sleep
import os

# Setting up the Arduino board
port = '/dev/cu.usbmodemfa1331'
board = Arduino(port)
# Need to give some time to pyFirmata and Arduino to synchronize
sleep(5)

# Start Iterator to avoid serial overflow
it = util.Iterator(board)
it.start()

# Assign a role and variable to analog pin 0 
a0 = board.get_pin('a:0:i')

# Running loop for ever
# This command executes loop body indefinitely until keyboard interrupt

try:
    while True:
        # Reading value on port a0
        p = a0.read()
        print p
except KeyboardInterrupt:
    board.exit()
    os._exit()
