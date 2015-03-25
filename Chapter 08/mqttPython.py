#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing

import paho.mqtt.client as mq
import time
import threading


def onMessage(mosq, obj, msg):
    print msg.topic+":"+msg.payload


def onPublish(mosq, obj, mid):
    pass


def publishTest():
    cli.publish("inTopic","From Python")
    threading.Timer(5, publishTest).start()

cli = mq.Client('mosquittoPython')
cli.on_message = onMessage
cli.on_publish = onPublish
cli.connect("10.0.0.20", 1883, 15)
cli.subscribe("outTopic", 0)
publishTest()
cli.loop_forever()


