#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import paho.mqtt.client as mq
import httplib


def onMessage(mosq, obj, msg):
    print msg.topic
    connection = httplib.HTTPConnection('10.0.0.20:8080')
    if msg.topic == "Arduino/motion":
        data = "motion:" + msg.payload
        connection.request('POST', '/data', data)
        postResult = connection.getresponse()
        print postResult
    elif msg.topic == "Arduino/humidity":
        data = "humidity:" + msg.payload
        connection.request('POST', '/data', data)
        postResult = connection.getresponse()
        print postResult
    else:
        pass
    connection.close()


def onPublish(mosq, obj, mid):
    pass


cli = mq.Client('mosquittoPython')
cli.on_message = onMessage
cli.on_publish = onPublish
cli.connect("10.0.0.20", 1883, 15)
cli.subscribe("Arduino/humidity", 0)
cli.subscribe("Arduino/motion", 0)
cli.loop_forever()


