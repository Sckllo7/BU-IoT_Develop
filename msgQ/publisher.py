#!/usr/bin/python

import json
import sys 
import Adafruit_DHT
import paho.mqtt.client as mqtt
import time
import os
import random

hostname = os.uname()[1]

while (1) :
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    temp = { 'hostname' : hostname,
             'name' : 'Temperature',
             'value' : temperature }

    humi = { 'hostname' : hostname,
             'name' : 'Humidity',
             'value' : humidity }

    jsonTemp = json.dumps(temp)
    jsonHumi = json.dumps(humi)

    mqttc = mqtt.Client("python_pub")
    mqttc.connect("buhadoop", 1883)

    if humidity is not None and temperature is not None:
            mqttc.publish("Home/Univer/Temp", jsonTemp)
            mqttc.publish("Home/Univer/Humi", jsonHumi)

    else:
            print 'Failed to get reading. Try again!'

    time.sleep(2)
    mqttc.disconnect()
#    time.sleep(random.randrange(1, 4))
