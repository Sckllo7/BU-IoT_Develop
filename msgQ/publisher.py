#!/usr/bin/python

import json
import sys 
import Adafruit_DHT
import paho.mqtt.client as mqtt
import time
import os
import random

hostname = os.uname()[1]
pHumidity = 0
pTemperature = 0
stamp = 0.0

while (1) :
    time.sleep(5)

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    temp = { 'hostname' : hostname,
             'name' : 'Temperature',
             'value' : temperature }

    humi = { 'hostname' : hostname,
             'name' : 'Humidity',
             'value' : humidity }

    jsonTemp = json.dumps(temp)
    jsonHumi = json.dumps(humi)

    if (humidity != pHumidity & temperature != pTemperature) | (time.time() - stamp) > 60 :
	swit = 3
    elif humidity != pHumidity & temperature == pTemperature :
	swit = 2
    elif humidity == pHumidity & temperature != pTemperature :
	swit = 1
    else
	continue;

    stamp = time.time()

    mqttc = mqtt.Client("python_pub")
    mqttc.connect("buhadoop", 1883)

    if humidity is not None and temperature is not None:
	    if swit == 3 :
		    mqttc.publish("Home/Univer/Temp", jsonTemp)
		    mqttc.publish("Home/Univer/Humi", jsonHumi)
	    elif swit == 2:
		    mqttc.publish("Home/Univer/Temp", jsonTemp)
	    elif swit == 1:
		    mqttc.publish("Home/Univer/Humi", jsonHumi)

    else:
            print 'Failed to get reading. Try again!'

    mqttc.disconnect()
