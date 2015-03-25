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

# Trying to create a channel on Xively if it doesn't exist already
try:
    datastream = feed.datastreams.get("Random")
except HTTPError as e:
    print "HTTPError({0}): {1}".format(e.errno, e.strerror)
    datastream = feed.datastreams.create("Random", tags="python")
    print "Creating 'Random' datastream"

# While loop to send data to Xively until manually code termination
while True:
    # Add a random value to the datastream
    randomValue = random.random()
    print "Latest value sent to 'Random' channel: " + str(randomValue)
    datastream.current_value = randomValue
    datastream.at = datetime.datetime.utcnow()

    # Update datastream with the random value
    try:
        datastream.update()
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)

    # Add delay between two consecutive entry to Xively
    time.sleep(10)

