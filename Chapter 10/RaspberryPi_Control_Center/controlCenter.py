#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import paho.mqtt.client as mq
import Tkinter
import time
import sys
import threading
import xively
from urllib2 import HTTPError


class controlCenterWindow(threading.Thread):
    def __init__(self):
        # Tkinter canvas
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.top.quit()

    def run(self):
        self.top = Tkinter.Tk()
        self.top.protocol("WM_DELETE_WINDOW", self.callback)
        self.top.title("Control Center")

        self.statusValue = Tkinter.StringVar()
        self.statusValue.set("Normal")
        self.tempValue = Tkinter.StringVar()
        self.tempValue.set('-')
        self.humdValue = Tkinter.StringVar()
        self.humdValue.set('-')
        self.lightValue = Tkinter.StringVar()
        self.lightValue.set('-')
        self.motionValue = Tkinter.StringVar()
        self.motionValue.set('No')

        Tkinter.Label(self.top, textvariable=self.statusValue, fg="blue").grid(row=1, column=1, columnspan=3)
        Tkinter.Label(self.top, text="Temperature :").grid(column=1, row=2)
        Tkinter.Label(self.top, text="Humidity :").grid(column=1, row=3)
        Tkinter.Label(self.top, text="Light :").grid(column=1, row=4)
        Tkinter.Label(self.top, text="Motion :").grid(column=1, row=5)
        TempLabel = Tkinter.Label(self.top, textvariable=self.tempValue)
        TempLabel.grid(column=2, row=2)
        HumdLabel = Tkinter.Label(self.top, textvariable=self.humdValue)
        HumdLabel.grid(column=2, row=3)
        LightLabel = Tkinter.Label(self.top, textvariable=self.lightValue)
        LightLabel.grid(column=2, row=4)
        MotionLabel = Tkinter.Label(self.top, textvariable=self.motionValue)
        MotionLabel.grid(column=2, row=5)

        TempUnitLabel = Tkinter.Label(self.top, text=" C")
        TempUnitLabel.grid(column=3, row=2)
        HumdUnitLabel = Tkinter.Label(self.top, text=" %")
        HumdUnitLabel.grid(column=3, row=3)
        LighUnitLabel = Tkinter.Label(self.top, text=" lx")
        LighUnitLabel.grid(column=3, row=4)
        self.top.mainloop()


def calculateStatus():
    if tempG > 45:
        if humdG > 80:
            status = "High Temperature and Humidity"
        elif humdG < 20:
            status = "High Temperature, Low Humidity"
        else:
            status = "High Temperature"
        setAlert(status)

    elif tempG < 5:
        if humdG > 80:
            status = "Low Temperature and Humidity"
        elif humdG < 20:
            status = "Low Temperature, Low Humidity"
        else:
            status = "Low Temperature"
        setAlert(status)
    else:
        if humdG > 80:
            status = "High Humidity"
            setCaution(status)
        elif humdG < 20:
            status = "Low Humidity"
            setCaution(status)
        else:
            status = "Normal"
            setNormal(status)


def checkBuzzerFromXively():
    try:
        datastreamBuzzer = feed.datastreams.get("Buzzer")
        buzzerValue = datastreamBuzzer.current_value
        buzzerValue = str(buzzerValue)
        cli.publish("MonitoringStation/buzzer", buzzerValue)
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        print "Requested channel doesn't exist"
    threading.Timer(30, checkBuzzerFromXively).start()


def setAlert(status):
    window.statusValue.set(status)
    datastreamStatus.current_value = "Alert"
    try:
        datastreamStatus.update()
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
    cli.publish("MonitoringStation/led", 'red')
    cli.publish("MonitoringStation/buzzer", 'ON')


def setCaution(status):
    window.statusValue.set(status)
    datastreamStatus.current_value = "Caution"
    try:
        datastreamStatus.update()
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
    cli.publish("MonitoringStation/led", 'yellow')


def setNormal(status):
    window.statusValue.set(status)
    datastreamStatus.current_value = "Normal"
    try:
        datastreamStatus.update()
    except HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
    cli.publish("MonitoringStation/led", 'off')


def onMessage(mosq, obj, msg):
    global tempG, humdG, lightG, motionG
    tempG = 22
    humdG = 50
    lightG = 100
    motionG = 1
    print "%-20s %d %s" % (msg.topic, msg.qos, msg.payload)
    if msg.topic == "MonitoringStation/temperature":
        tempG = float(msg.payload)
        window.tempValue.set(tempG)
        datastreamTemp.current_value = tempG
        try:
            datastreamTemp.update()
        except HTTPError as e:
            print "HTTPError({0}): {1}".format(e.errno, e.strerror)
    if msg.topic == "MonitoringStation/humidity":
        humdG = float(msg.payload)
        window.humdValue.set(humdG)
        datastreamHumd.current_value = humdG
        try:
            datastreamHumd.update()
        except HTTPError as e:
            print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        calculateStatus()
    if msg.topic == "MonitoringStation/motion":
        motionG = float(msg.payload)
        datastreamMotion.current_value = motionG
        try:
            datastreamMotion.update()
        except HTTPError as e:
            print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        if motionG == 1:
            motionMes = "Yes"
        else:
            motionMes = "No"
        window.motionValue.set(motionMes)
    if msg.topic == "MonitoringStation/light":
        lightG = float(msg.payload)
        datastreamLight.current_value = lightG
        try:
            datastreamLight.update()
        except HTTPError as e:
            print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        window.lightValue.set(lightG)


def onPublish(mosq, obj, mid):
    pass


window = controlCenterWindow()

# Your Xively account credentials 
FEED_ID = "1914657379"
API_KEY = "18rnjbgSgCJHTWcf56Kq28TfLQ12anOp0ivg2w4BmitIZ8uF"

# Initializing Xively api and feed
api = xively.XivelyAPIClient(API_KEY)
feed = api.feeds.get(FEED_ID)

# Setting up datastreams for Xively
try:
    datastreamTemp = feed.datastreams.get("Temperature")
except HTTPError as e:
    print "HTTPError({0}): {1}".format(e.errno, e.strerror)
    datastreamTemp = feed.datastreams.create("Temperature", tags="C")
    print "Creating new channel 'Temperature'"

try:
    datastreamHumd = feed.datastreams.get("Humidity")
except HTTPError as e:
    print "HTTPError({0}): {1}".format(e.errno, e.strerror)
    datastreamHumd = feed.datastreams.create("Humidity", tags="%")
    print "Creating new channel 'Humidity'"

try:
    datastreamLight = feed.datastreams.get("Light")
except HTTPError as e:
    print "HTTPError({0}): {1}".format(e.errno, e.strerror)
    datastreamLight = feed.datastreams.create("Light", tags="lx")
    print "Creating new channel 'Light'"

try:
    datastreamMotion = feed.datastreams.get("Motion")
except HTTPError as e:
    print "HTTPError({0}): {1}".format(e.errno, e.strerror)
    datastreamMotion = feed.datastreams.create("Motion", tags="motion")
    print "Creating new channel 'Motion'"

try:
    datastreamStatus = feed.datastreams.get("Status")
except HTTPError as e:
    print "HTTPError({0}): {1}".format(e.errno, e.strerror)
    datastreamStatus = feed.datastreams.create("Status", tags="status")
    print "Creating new channel 'Status'"

cli = mq.Client('ControlCenter')
cli.on_message = onMessage
cli.on_publish = onPublish

cli.connect("10.0.0.18", 1883, 15)

cli.subscribe("MonitoringStation/temperature", 0)
cli.subscribe("MonitoringStation/humidity", 0)
cli.subscribe("MonitoringStation/motion", 0)
cli.subscribe("MonitoringStation/light", 0)
cli.subscribe("MonitoringStation/buzzer", 0)
cli.subscribe("MonitoringStation/led", 0)
checkBuzzerFromXively()
cli.loop_forever()
