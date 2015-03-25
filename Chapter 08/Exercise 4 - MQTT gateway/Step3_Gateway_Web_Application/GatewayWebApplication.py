#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import web
import datetime
from web import form
from time import sleep
from urllib2 import HTTPError

global humidity, motion
humidity = 100
temperature = 22

# Defining template and urls for web.py
render = web.template.render('templates')

urls = (
'/', 'index',
'/data', 'data',
)


class index:
    submit_form = form.Form(
        form.Button('Refresh',
                    type="submit",
                    description='refresh')
    )

    # GET function
    def GET(self):
        f = self.submit_form()
        return render.base(f, humidity, motion)

    # POST function
    def POST(self):
        f = self.submit_form()
        return render.base(f, humidity, motion)


class data:

    def POST(self):
        global motion, humidity
        i = web.input()
        data = web.data()
        data = data.split(":")
        if data[0] == "humidity":
            humidity = data[1]
        elif data[0] == "motion":
            motion = data[1]
        else:
            pass
        return "Ok"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
