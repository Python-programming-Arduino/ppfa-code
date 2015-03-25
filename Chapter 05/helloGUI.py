#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import Tkinter

# Initialize main windows with title and size
top = Tkinter.Tk()
top.title("Hello GUI")
top.minsize(200, 30)

# Label widget
helloLabel = Tkinter.Label(top,
                           text="Hello World!")
helloLabel.pack()

# Start and open the window
top.mainloop()
