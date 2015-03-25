#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing


# Define the action associated with button press
def onStartButtonPress():
    timePeriod = timePeriodEntry.get()
    timePeriod = float(timePeriod)
    ledBrightness = brightnessScale.get()
    ledBrightness = float(ledBrightness)
    startButton.config(state=Tkinter.DISABLED)
    ledPin.write(ledBrightness / 100.0)
    sleep(timePeriod)
    ledPin.write(0)
    startButton.config(state=Tkinter.ACTIVE)

import Tkinter
import pyfirmata
from time import sleep

# Associate port and board with pyFirmata
port = '/dev/cu.usbmodemfa1331'
board = pyfirmata.Arduino(port)
sleep(5)
# Define led pins
ledPin = board.get_pin('d:11:o')

# Initialize main windows with title and size
top = Tkinter.Tk()
top.title("Grid example")

# Text field entry to provide LED on time
timePeriodEntry = Tkinter.Entry(top, bd=5)
timePeriodEntry.grid(column=1, row=1)
timePeriodEntry.focus_set()
Tkinter.Label(top,
              text="Time (seconds)").grid(column=2, row=1)

# Scale to specify LED brightness
brightnessScale = Tkinter.Scale(top,
                                from_=0, to=100,
                                orient=Tkinter.HORIZONTAL)
brightnessScale.grid(column=1, row=2)
Tkinter.Label(top,
              text="Brightness (%)").grid(column=2, row=2)

# Create a button on main window and associate it with above method
startButton = Tkinter.Button(top,
                             text="Start",
                             command=onStartButtonPress)
startButton.grid(column=1, row=3)

# Create Exit button and destroy the window
exitButton = Tkinter.Button(top,
                            text="Exit",
                            command=top.quit)
exitButton.grid(column=2, row=3)

# Start and open the window
top.mainloop()
