#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import xively
import datetime
import time
import random
from urllib2 import HTTPError

# Your Xively account credentials 
FEED_ID = "1649696305"
API_KEY = "OKJacI8hWH46jiDKh6oodaJQWatpdPEELl0Nm25UOG5GxSFY"

# Initializing Xively api and feed
api = xively.XivelyAPIClient(API_KEY)
feed = api.feeds.get(FEED_ID)

# While loop to send data to Xively until manually code termination
while True:
    # Trying to create a channel on Xively if it doesn't exist already
    try:
        datastream = feed.datastreams.get("Random")
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        print "Requested channel doesn't exist"
    # Update datastream with the random value
    try:
        latestValue = datastream.current_value
        print "Latest received value from 'Random' channel: " + str(latestValue)
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)

    # Add delay between two consecutive entry to Xively
    time.sleep(10)

