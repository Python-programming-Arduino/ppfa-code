#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import Tkinter
import pyfirmata
from time import sleep


# Define the action associated with button press
def onStartButtonPress():
    startButton.config(state=Tkinter.DISABLED)
    ledPin.write(1)
    # LED is on for fix amount of time specified below
    sleep(5)
    ledPin.write(0)
    startButton.config(state=Tkinter.ACTIVE)


# Associate port and board with pyFirmata
port = '/dev/cu.usbmodemfa1331'
board = pyfirmata.Arduino(port)
sleep(5)

# Define led pins
ledPin = board.get_pin('d:11:o')

# Initialize main windows with title and size
top = Tkinter.Tk()
top.title("Blink LED using button")
top.minsize(300, 30)

# Create a button on main window and associate it with above method
startButton = Tkinter.Button(top,
                             text="Start",
                             command=onStartButtonPress)
startButton.pack()

# Start and open the window
top.mainloop()
