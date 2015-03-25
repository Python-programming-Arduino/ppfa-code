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
FEED_ID = "1914657379"
API_KEY = "18rnjbgSgCJHTWcf56Kq28TfLQ12anOp0ivg2w4BmitIZ8uF"

# Initializing Xively api and feed
api = xively.XivelyAPIClient(API_KEY)
feed = api.feeds.get(FEED_ID)


def fetchTempXively():
    try:
        datastreamTemp = feed.datastreams.get("Temperature")
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        print "Requested channel doesn't exist"
    return datastreamTemp.current_value


def fetchHumdXively():
    try:
        datastreamHumd = feed.datastreams.get("Humidity")
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        print "Requested channel doesn't exist"
    return datastreamHumd.current_value


def fetchMotionXively():
    try:
        datastreamMotion = feed.datastreams.get("Motion")
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        print "Requested channel doesn't exist"
    return datastreamMotion.current_value


def fetchLightXively():
    try:
        datastreamLight = feed.datastreams.get("Light")
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        print "Requested channel doesn't exist"
    return datastreamLight.current_value


def fetchStatusXively():
    try:
        datastreamStatus = feed.datastreams.get("Status")
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        print "Requested channel doesn't exist"
    return datastreamStatus.current_value


global status, temperature, humidity, motion, light
temperature = fetchTempXively()
humidity = fetchHumdXively()
motion = fetchMotionXively()
light = fetchLightXively()
status = fetchStatusXively()

# Defining template and urls for web.py
render = web.template.render('templates')

urls = ('/',
        'index')


def setBuzzer(statusTemp):
    try:
        datastream = feed.datastreams.get("Buzzer")
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        datastream = feed.datastreams.create("Buzzer",
                                             tags="buzzer")
        print "Creating new Channel 'Buzzer"
    datastream.current_value = statusTemp
    try:
        datastream.update()
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)


# Index class for web.py
class index:
    # Defining form
    submit_form = form.Form(
        form.Button('btn', value="refresh", html="Refresh"),
        form.Button('btn', value="buzzerOff", html="Buzzer Off")
    )
    # GET function
    def GET(self):
        f = self.submit_form()
        return render.base(f, status, temperature, humidity, light, motion)

    # POST function
    def POST(self):
        f = self.submit_form()
        # f.validates()
        inputData = web.input()
        temperature = fetchTempXively()
        humidity = fetchHumdXively()
        motion = fetchMotionXively()
        light = fetchLightXively()
        status = fetchStatusXively()
        if inputData.btn == "buzzerOff":
            setBuzzer("OFF")
        return render.base(f, status, temperature, humidity, light, motion)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
