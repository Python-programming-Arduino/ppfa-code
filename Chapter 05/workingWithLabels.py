#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import Tkinter
import pyfirmata


# Define the action associated with Start button press
def onStartButtonPress():
    while True:
        if flag.get():
            analogReadLabel.config(text=str(a0.read()))
            analogReadLabel.update_idletasks()
            top.update()
        else:
            break
    board.exit()
    top.destroy()


# Define the action associated with Exit button press
def onExitButtonPress():
    flag.set(False)


# Associate port and board with pyFirmata
port = '/dev/cu.usbmodemfa1331'
board = pyfirmata.Arduino(port)

# Using iterator thread to avoid buffer overflow
it = pyfirmata.util.Iterator(board)
it.start()

# Define pins 
# Assign a role and variable to analog pin 0 
a0 = board.get_pin('a:0:i')

# Initialize main windows with title and size
top = Tkinter.Tk()
top.title("Reading Analog pins")

# Create Label to read analog input
descriptionLabel = Tkinter.Label(top, text="Potentiometer input:- ")
descriptionLabel.grid(column=1, row=1)

# Create Label to read analog input
analogReadLabel = Tkinter.Label(top, text="Press Start..")
analogReadLabel.grid(column=2, row=1)

# Setting flag to toggle read option
flag = Tkinter.BooleanVar(top)
flag.set(True)

# Create Start button and associate with onStartButtonPress method
startButton = Tkinter.Button(top,
                             text="Start",
                             command=onStartButtonPress)
startButton.grid(column=1, row=2)

# Create Stop button and associate with onStopButtonPress method
exitButton = Tkinter.Button(top,
                            text="Exit",
                            command=onExitButtonPress)
exitButton.grid(column=2, row=2)

# Start and open the window
top.mainloop()