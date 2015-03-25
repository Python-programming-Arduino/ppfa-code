#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import csv

with open('example.csv', 'r') as file:
    r = csv.reader(file)
    for row in r:
        print row
