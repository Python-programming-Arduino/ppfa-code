#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing


import serial
import sys
import numpy as np
import Tkinter
from matplotlib import pyplot, rcParams

# port = serial.Serial('/dev/ttyACM0',9600, timeout=1)
port = serial.Serial('COM5', 9600, timeout=1)

# Tkinter canvas
top = Tkinter.Tk()
top.title("Tkinter + matplotlib")
top.minsize(320, 200)

# Create flag to work with indefinite while loop
flag = Tkinter.BooleanVar(top)
flag.set(True)


def cleanText(data):
    data = data.replace("\r\n", "")
    return data


def onStartButtonPress():
    while True:
        if flag.get():
            line = port.readline()
            reading = line.split(':')
            # print reading
            if len(reading) == 2:
                for i in range(2):
                    if reading[0] == "Temperature(C)":
                        TempLabel.config(text=cleanText(reading[1]), font=("Helvetica", 20))
                        TempUnitLabel.config(text="C", font=("Helvetica", 20))
                        TempUnitLabel.update_idletasks()
                    if reading[0] == "Temperature(F)":
                        TempLabel.config(text=cleanText(reading[1]), font=("Helvetica", 20))
                        TempUnitLabel.config(text="F", font=("Helvetica", 20))
                        TempUnitLabel.update_idletasks()
                    if reading[0] == "Humidity(%)":
                        HumdLabel.config(text=cleanText(reading[1]),
                                         font=("Helvetica", 20))
                        pData.append(float(reading[1]))
                        del pData[0]
                    if reading[0] == "Light(lx)":
                        LighLabel.config(text=cleanText(reading[1]), font=("Helvetica", 20))
                    if reading[0] == "Flag":
                        print reading[1]
                        if int(reading[1]) == 1:
                            try:
                                l1.set_xdata(np.arange(len(pData)))
                                l1.set_ydata(pData)  # update the data
                                pyplot.ylim([0, 100])
                                pyplot.draw()  # update the plot
                            except:
                                pyplot.figure(figsize=(4, 3))
                                pyplot.title('Humidity')
                                ax1 = pyplot.axes()
                                l1, = pyplot.plot(pData)
                                pyplot.ylim([0, 100])
                        if int(reading[1]) == 0:
                            try:
                                pyplot.close('all')
                                l1 = None
                            except:
                                continue
            port.flushInput()
            top.update()
        else:
            flag.set(True)
            break


def onExitButtonPress():
    print "Exiting...."
    flag.set(False)
    port.close()
    top.quit()
    top.destroy()
    print "Done."
    sys.exit()

pyplot.ion()
rcParams['toolbar'] = 'None'
pData = [0] * 25

Tkinter.Label(top,
              text="Temperature",
              font=("Helvetica", 20)).grid(column=1, row=1)
Tkinter.Label(top,
              text="Humidity",
              font=("Helvetica", 20)).grid(column=1, row=2)
Tkinter.Label(top,
              text="Light",
              font=("Helvetica", 20)).grid(column=1, row=3)

TempLabel = Tkinter.Label(top, text=" ")
TempLabel.grid(column=2, row=1)
HumdLabel = Tkinter.Label(top, text=" ")
HumdLabel.grid(column=2, row=2)
LighLabel = Tkinter.Label(top, text=" ")
LighLabel.grid(column=2, row=3)

TempUnitLabel = Tkinter.Label(top, text=" ")
TempUnitLabel.grid(column=3, row=1)
HumdUnitLabel = Tkinter.Label(top,
                              text="%",
                              font=("Helvetica", 20))
HumdUnitLabel.grid(column=3, row=2)
LighUnitLabel = Tkinter.Label(top,
                              text="lx",
                              font=("Helvetica", 20))
LighUnitLabel.grid(column=3, row=3)

# Create Start button and associate with onStartButtonPress method
StartButton = Tkinter.Button(top,
                             text="Start",
                             command=onStartButtonPress,
                             font=("Helvetica", 20))
StartButton.grid(column=1, row=4)

# Create Exit button and destroy the window
ExitButton = Tkinter.Button(top,
                            text="Exit",
                            command=onExitButtonPress,
                            font=("Helvetica", 20))
ExitButton.grid(column=2, row=4)

top.mainloop()
