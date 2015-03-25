#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import csv

data = [[1, 2, 3], ['a', 'b', 'c'], ['Python', 'Arduino', 'Programming']]

with open('example.csv', 'w') as f:
    w = csv.writer(f)
    for row in data:
        w.writerow(row)