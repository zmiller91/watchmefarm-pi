__author__ = 'zmiller'

import os
import serial
import time
import configuration as conf
import shared
import json
import requests

def post(url, payload):
    try:
        return requests.post(url, data=json.dumps(payload))
    except  e:
        return e.message

def sendSensorReading(component, instruction, value):

    url = conf.BASE_URL + "api/poll"
    reading = {"component": component, "instruction": instruction, "value": value};
    postResponse = post(url, reading)

    ## TODO: handle failure
    if postResponse.status_code >= 400:
        print postResponse.status_code
        print postResponse.content

def sendComponentStatus(component, instruction, state):

    url = conf.BASE_URL + "api/states"
    state = {"component": component, "instruction": instruction, "state": state};
    postResponse = post(url, state)

    ## TODO: handle failure
    if postResponse.status_code >= 400:
        print postResponse.status_code
        print postResponse.content

def receiveMessage(line):

    # A serial message in the format NNNN:NNNN:NNNN is either a sensor reading
    # or a component notification
    parts = line.split(":")
    if len(parts) == 3:

        # It's a poll
        if int(parts[1]) == 2000:
            sendSensorReading(parts[0], parts[1], parts[2])

        # It's a component
        elif int(int(parts[0]) / 1000 == 1):
            sendComponentStatus(parts[0], parts[1], parts[2])

        else:
            print line
    # Must be something else, just print it
    else:
        print line

def sendMessage(file):

    path = conf.PATH + "/" + file
    f = open(path)
    configuration = f.read()
    f.close()
    os.remove(path)

    print "Writing: " + configuration
    ser.write(configuration + "\n")

start = shared.curTime()
ser = serial.Serial('COM4', 9600, timeout=1)
responded = True
while True:

    try:
        # Read serial and handle messages
        line = ser.readline().rstrip("\r\n")
        if len(line) > 0:
            receiveMessage(line)
            if "Received: " in line:
                responded = True

        # Check if new configuration data exists
        if responded and os.path.isdir(conf.PATH):
            files = os.listdir(conf.PATH)
            if len(files) > 0:
                sendMessage(files[0])
                responded = False

        time.sleep(.10)

    except Exception as e:
        print str(e)