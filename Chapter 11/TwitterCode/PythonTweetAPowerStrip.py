#!/usr/bin/python

# This code is supporting material for the book
# Python Programming for Arduino
# by Pratik Desai
# published by PACKT Publishing


import twitter
from time import sleep
import threading
import paho.mqtt.client as mq

api = twitter.Api(consumer_key='ElrWuAImGZNoBy6WiSHVOXe7X',
                  consumer_sret='N7SWj2hiVLMRLKs0NIw9JxDPlvJ05TzJ5CndtVofyCW908Sl3a',
                  access_token_key='2806636166-2NdgLd2is06uxxaCweuSgPd0Vnn9PZnwJ383kI5',
                  access_secret='mAVkd1swPcXwLleUOaWIBWN38TYwzngjwcm9zZWx4488w')


def onMessage(mosq, obj, msg):
    if msg.topic == "PowerStrip/statusreport":
        print msg.payload
        api.PostUpdate(msg.payload)


def onPublish(mosq, obj, mid):
    pass


cli = mq.Mosquitto('TweetCenter')
cli.on_message = onMessage
cli.on_publish = onPublish

cli.connect("10.0.0.20", 1883, 15)

cli.subscribe("PowerStrip/statusreport", 0)


class checkTweet(threading.Thread):
    def __init__(self):
        # Tkinter canvas
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.top.quit()

    def run(self):
        global lastTweetId
        with open('lastTweetID.txt', 'w+') as fh:
            lastTweetId = fh.readline()
            print "Initializing with ID: " + lastTweetId
        while True:
            statuses = api.GetHomeTimeline()
            currentStatus = statuses[0]
            if lastTweetId != str(currentStatus.id):
                lastTweetId = str(currentStatus.id)
                print "Updated file with ID: " + lastTweetId
                with open('lastTweetID.txt', 'w+') as fh:
                    fh.write(lastTweetId)
                    currentStatusText = currentStatus.text
                    print currentStatusText
                    if "#fan" in currentStatusText.lower():
                        if "#on" in currentStatusText.lower():
                            cli.publish("PowerStrip/fan", "on")
                        if "#off" in currentStatusText.lower():
                            cli.publish("PowerStrip/fan", "off")
                    if "#lamp" in currentStatusText.lower():
                        if "#on" in currentStatusText.lower():
                            cli.publish("PowerStrip/lamp", "on")
                        if "#off" in currentStatusText.lower():
                            cli.publish("PowerStrip/lamp", "off")
                    if "#toaster" in currentStatusText.lower():
                        if "#on" in currentStatusText.lower():
                            cli.publish("PowerStrip/toaster", "on")
                        if "#off" in currentStatusText.lower():
                            cli.publish("PowerStrip/toaster", "off")
                    if "#coffee" in currentStatusText.lower():
                        if "#on" in currentStatusText.lower():
                            cli.publish("PowerStrip/coffeemaker", "on")
                        if "#off" in currentStatusText.lower():
                            cli.publish("PowerStrip/coffeemaker", "off")
                    if "#status" in currentStatusText.lower():
                        if "#get" in currentStatusText.lower():
                            cli.publish("PowerStrip/statuscheck", "get")
            else:
                print "No new update."
            sleep(60)


checkTweet()
cli.loop_forever()

