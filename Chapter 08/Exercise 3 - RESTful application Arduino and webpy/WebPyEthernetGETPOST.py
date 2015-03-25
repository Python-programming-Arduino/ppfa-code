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
    '/data','data',
)

render = web.template.render('templates/')

class index:
    global temperature
    temperature = 25
    global sensorType
    sensorType = "Humidity"
    submit_form = form.Form(
        form.Dropdown('dropdown',[('Humidity','Humidity'),('Motion','Motion')]),
        form.Button('submit', type="submit", description='submit')        
        )
    def GET(self):       
        f = self.submit_form()
        f.validates()
        return render.base(f,"Humidity", str(humidity)+" %")

    def POST(self):
        global  sensorType
        f = self.submit_form()
        f.validates()
        if f['dropdown'].value == "Humidity":
            sensorType = "Humidity"
            return render.base(f, "Humidity", str(humidity)+" %")
        else:
            sensorType = "Motion"
            return render.base(f, "Motion", motion)
        
class data:

    def GET(self):
        print sensorType
        return sensorType
    def POST(self):
        global humidity
        global motion
        i = web.input()
        data = web.data()
        data = data.split()[1]
        if sensorType == "Humidity":
            humidity = relativeHumidity(data,temperature)
            print humidity
            return humidity
        else:
            motion = data
            print motion
            return motion

def relativeHumidity(data, temperature):
    volt = float(data)/1024 * 5.0
    sensorRH = 161.0 * volt / 5.0 - 25.0
    trueRH = sensorRH / (1.0546 - 0.0026 * temperature)
    return trueRH
   
if __name__ == '__main__':

    app = web.application(urls, globals())
    app.run()
