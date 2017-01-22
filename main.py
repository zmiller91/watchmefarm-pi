__author__ = 'zmiller'

import os
import serial
import time
import configuration
import shared

def receiveMessage(line):
    print line

def sendMessage(file):
    path = configuration.PATH + "/" + file
    f = open(path)
    conf = f.read()
    f.close()
    os.remove(path)
    print "Writing: " + conf
    ser.write(conf + "\n")

start = shared.curTime()
ser = serial.Serial('COM4', 9600, timeout=1)
responded = True
while True:

    try:
        # Read serial and handle messages
        line = ser.readline().rstrip("\r\n")
        if len(line) > 0:
            receiveMessage(line)
            responded = True

        # Check if new configuration data exists
        if responded and os.path.isdir(configuration.PATH):
            files = os.listdir(configuration.PATH)
            if len(files) > 0:
                sendMessage(files[0])
                responded = False

        time.sleep(.10)

    except Exception as e:
        print str(e)