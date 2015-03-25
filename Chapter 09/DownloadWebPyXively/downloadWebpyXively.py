#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import web
import xively
import datetime
from web import form
from time import sleep
from urllib2 import HTTPError

# Your Xively account credentials 
FEED_ID = "1649696305"
API_KEY = "OKJacI8hWH46jiDKh6oodaJQWatpdPEELl0Nm25UOG5GxSFY"

# Initializing Xively api and feed
api = xively.XivelyAPIClient(API_KEY)
feed = api.feeds.get(FEED_ID)

# Defining template and urls for web.py
render = web.template.render('templates')

urls = ('/', 'index')


# Index class for web.py
def updateHumidityChannel(humidity):
    try:
        datastream = feed.datastreams.get("Humidity")
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        datastream = feed.datastreams.create("Humidity", tags="%")
        print "Creating Humidity datastream."
    datastream.current_value = humidity
    datastream.at = datetime.datetime.utcnow()
    try:
        datastream.update()
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)


def relativeHumidity(data, temperature):
    volt = float(data) / 1024 * 5.0
    sensorRH = 161.0 * volt / 5.0 - 25.0
    trueRH = sensorRH / (1.0546 - 0.0026 * temperature)
    return trueRH


class index:
    global temperature
    temperature = 22
    global humidity
    humidity = 0
    # Defining form
    submit_form = form.Form(
        form.Textbox('Temperature', description='Temperature'),
        form.Button('submit', type="submit", description='submit')
    )
    # GET function
    def GET(self):
        f = self.submit_form()
        f.validates()
        return render.base(f, temperature, humidity)

    # POST function
    def POST(self):
        f = self.submit_form()
        f.validates()
        temperature = float(f['Temperature'].value)
        # Trying to create a channel on Xively if it doesn't exist already
        try:
            datastream = feed.datastreams.get("HumidityRaw")
        except HTTPError as e:
            print "HTTPError({0}): {1}".format(e.errno, e.strerror)
            print "Requested channel doesn't exist"
        # Update datastream with the random value
        try:
            latestValue = datastream.current_value
            humidity = relativeHumidity(latestValue, temperature)
            updateHumidityChannel(humidity)
            return render.base(f, temperature, humidity)
        except HTTPError as e:
            print "HTTPError({0}): {1}".format(e.errno, e.strerror)
            print "Please refresh the page."


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
