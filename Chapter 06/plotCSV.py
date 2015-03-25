#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing


import csv
from matplotlib import pyplot

i = []
mValues = []
pValues = []

with open('SensorDataStore.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader, None)
    for row in reader:
        i.append(int(row[0]))
        pValues.append(float(row[1]))
        if row[2] == 'True':
            mValues.append(1)
        else:
            mValues.append(0)

pyplot.subplot(2, 1, 1)
pyplot.plot(i, pValues, '-')
pyplot.title('Line plot - ' + header[1])
pyplot.xlim([1, 25])
pyplot.xlabel('X Axis')
pyplot.ylabel('Y Axis')

pyplot.subplot(2, 1, 2)
pyplot.bar(i, mValues)
pyplot.title('Bar chart - ' + header[2])
pyplot.xlim([1, 25])
pyplot.xlabel('X Axis')
pyplot.ylabel('Y Axis')

pyplot.tight_layout()

pyplot.show()