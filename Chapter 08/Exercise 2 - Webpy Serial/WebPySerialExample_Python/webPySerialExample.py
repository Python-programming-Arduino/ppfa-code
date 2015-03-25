#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import web
from web import form
import serial

port = serial.Serial('/dev/tty.usbmodemfa1331', 9600, timeout=1)

render = web.template.render('templates')

urls = (
'/', 'index')


class index:
    submit_form = form.Form(
    form.Textbox('Temperature', description='Temperature'),
    form.Button('submit', type="submit", description='submit')
    )

    def GET(self):
        f = self.submit_form()
        f.validates()
        line = port.readline()
        if line:
            data = float(line)
            humidity = relativeHumidity(line, 25)
            return render.base(f, humidity)
        else:
            return render.base(f, "Not valid data")

    def POST(self):
        f = self.submit_form()
        f.validates()
        temperature = f['Temperature'].value
        line = port.readline()
        if line:
            data = float(line)
            humidity = relativeHumidity(line, float(temperature))
            return render.base(f, humidity)
        else:
            return render.base(f, "Not valid data")


def relativeHumidity(data, temperature):
    volt = float(data) / 1024 * 5.0
    sensorRH = 161.0 * volt / 5.0 - 25.0
    trueRH = sensorRH / (1.0546 - 0.0026 * temperature)
    return trueRH


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
