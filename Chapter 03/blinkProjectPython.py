#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

# import required libraries
import pyfirmata
from time import sleep


# define custom function to perform Blink action
def blinkLED(pin, message):
    print message
    board.digital[pin].write(1)
    sleep(1)
    board.digital[pin].write(0)
    sleep(1)
    pass

# Associate port and board with pyFirmata
port = '/dev/cu.usbmodemfa1321'
board = pyfirmata.Arduino(port)

# Using iterator thread to avoid buffer overflow
it = pyfirmata.util.Iterator(board)
it.start()

# Define pins 
pirPin = board.get_pin('d:7:i')
redPin = 11
greenPin = 12

# Check for PIR sensor input
while True:
    # Ignore case when receiving None value from pin
    while pirPin.read() is None:
        pass

    if pirPin.read() is True:
        # Perform Blink using custom function
        blinkLED(redPin, "Motion Detected")

    else:
        # Perform Blink using custom function
        blinkLED(greenPin, "No motion Detected")

# Release the board        
board.exit()
