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
class index:
    # Defining form
    submit_form = form.Form(
        form.Textbox('Channel', description='Channel'),
        form.Textbox('Value', description='Value'),
        form.Button('submit', type="submit", description='submit')
    )

    # GET function
    def GET(self):
        f = self.submit_form()
        f.validates()
        return render.base(f)

    # POST function
    def POST(self):
        f = self.submit_form()
        f.validates()
        channel = f['Channel'].value
        value = f['Value'].value
        # Trying to create a channel on Xively if it doesn't exist already
        try:
            datastream = feed.datastreams.get(channel)
        except HTTPError as e:
            print "HTTPError({0}): {1}".format(e.errno, e.strerror)
            datastream = feed.datastreams.create(channel, tags="ManualPython")
            print "Creating a new datastream"
        # Add a random value to the datastream
        datastream.current_value = float(value)
        datastream.at = datetime.datetime.utcnow()
        # Update datastream with the random value
        try:
            datastream.update()
            return render.base(f)
        except HTTPError as e:
            return "Please refresh tha page. HTTPError({0}): {1}".format(e.errno, e.strerror)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
