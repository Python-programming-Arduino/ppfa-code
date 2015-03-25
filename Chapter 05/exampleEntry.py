#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing


# Define the action associated with button press
def onStartButtonPress():
    # Value for delay is obtained from the Entry widget input
    timePeriod = timePeriodEntry.get()
    timePeriod = float(timePeriod)
    startButton.config(state=Tkinter.DISABLED)
    ledPin.write(1)
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
top.title("Specify time using Entry")

# Text field entry to provide LED on time
timePeriodEntry = Tkinter.Entry(top,
                                bd=5,
                                width=25)
timePeriodEntry.pack()
timePeriodEntry.focus_set()

# Create a button on main window and associate it with above method
startButton = Tkinter.Button(top,
                             text="Start",
                             command=onStartButtonPress)
startButton.pack()

# Start and open the window
top.mainloop()
