#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing


# Define custom function to perform Blink action
def blinkLED(pin, message):
    MotionLabel.config(text=message)
    MotionLabel.update_idletasks()
    top.update()
    pin.write(1)
    sleep(1)
    pin.write(0)
    sleep(1)


# Define the action associated with Start button press
def onStartButtonPress():
    while True:
        if flag.get():
            if pirPin.read() is True:
                blinkLED(redPin, "Motion Detected")
            else:
                blinkLED(greenPin, "No motion Detected")
        else:
            break
    board.exit()
    top.destroy()


def onExitButtonPress():
    flag.set(False)

import Tkinter
import pyfirmata
from time import sleep

# Associate port and board with pyFirmata
port = '/dev/cu.usbmodemfa1331'
board = pyfirmata.Arduino(port)

# Using iterator thread to avoid buffer overflow
it = pyfirmata.util.Iterator(board)
it.start()

# Define pins 
pirPin = board.get_pin('d:8:i')
redPin = board.get_pin('d:10:o')
greenPin = board.get_pin('d:11:o')
pirPin.read()

# Initialize main windows with title and size
top = Tkinter.Tk()
top.title("First Project")

# Create Label to for motion detection
MotionLabel = Tkinter.Label(top, text="Press Start..")
MotionLabel.grid(column=1, row=1)

# Create flag to work with indefinite while loop
flag = Tkinter.BooleanVar(top)
flag.set(True)

# Create Start button and associate it with onStartButtonPress method
StartButton = Tkinter.Button(top,
                             text="Start",
                             command=onStartButtonPress)
StartButton.grid(column=1, row=2)

# Create Stop button and associate it with onStopButtonPress method
StopButton = Tkinter.Button(top,
                            text="Exit",
                            command=onExitButtonPress)
StopButton.grid(column=2, row=2)

# Start and open the window
top.mainloop()
