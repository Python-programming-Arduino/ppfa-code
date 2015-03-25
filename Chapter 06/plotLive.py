#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing


from matplotlib import pyplot
import pyfirmata
from time import sleep

# Associate port and board with pyFirmata
port = '/dev/cu.usbmodemfa1321'
board = pyfirmata.Arduino(port)

# Using iterator thread to avoid buffer overflow
it = pyfirmata.util.Iterator(board)
it.start()

# Assign a role and variable to analog pin 0 
a0 = board.get_pin('a:0:i')

pyplot.ion()

pData = [0.0] * 25
fig = pyplot.figure()
pyplot.title('Real-time Potentiometer reading')
ax1 = pyplot.axes()
l1, = pyplot.plot(pData)
pyplot.ylim([0, 1])

while True:
    try:
        sleep(1)
        pData.append(float(a0.read()))
        pyplot.ylim([0, 1])
        del pData[0]
        l1.set_xdata([i for i in xrange(25)])
        l1.set_ydata(pData)  # update the data
        pyplot.draw()  # update the plot
    except KeyboardInterrupt:
        board.exit()
        break
