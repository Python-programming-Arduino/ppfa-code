#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import web
from web import form

render = web.template.render('templates')
urls = ( 
    '/', 'index',
    '/data', 'data',
)

render = web.template.render('templates/')


class index:
    global temperature
    temperature = 25
    submit_form = form.Form(
        form.Textbox('Temperature', description = 'Temperature'),
        form.Button('submit', type="submit", description='submit')        
        )

    def GET(self):       
        f = self.submit_form()
        f.validates()
        return render.base(f, humidity)

    def POST(self):
        global temperature
        f = self.submit_form()
        f.validates()
        if not f['Temperature'].value:
            temperature = 25.0
        else:
            temperature = float(f['Temperature'].value)
        return render.base(f, humidity)
class data:

    def POST(self):
        global humidity
        i = web.input()
        data = web.data()
        data = data.split()[1]
        humidity = relativeHumidity(data,temperature)
        return humidity


def relativeHumidity(data, temperature):
    volt = float(data)/1024 * 5.0
    sensorRH = 161.0 * volt / 5.0 - 25.0
    trueRH = sensorRH / (1.0546 - 0.0026 * temperature)
    return trueRH


if __name__ == '__main__':

    app = web.application(urls, globals())
    app.run()
