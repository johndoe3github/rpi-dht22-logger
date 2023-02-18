#!/usr/bin/env python
#Here's a simple logging example that just logs to a file.
#In order, it creates a Logger instance, then a FileHandler and a Formatter. It attaches the Formatter to the FileHandler, then the FileHandler to the Logger.
#20220206 Added a handler that writes to a file, making a new file at midnight and keeping 366 backups
#20220208 20u11 python 3 = fixed print ""
#20230105 17u22 adapted for dht22 sensor (do install adafruit first)

import logging
import logging.handlers
import sys
import os
import time
import datetime
import glob
from time import strftime
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#20230218 14u11 edit to your dht22 device path and name
temp_sensor = '/sys/bus/w1/devices/28-000007268a94/w1_slave'

logger = logging.getLogger('temploggerrotatedatetag')

dateTag = datetime.datetime.now().strftime("%Y%m%d")

#20230218 14u12 edit your home folder name
logging.basicConfig(filename="/home/your-user-name/templogger/logs/temploggerrotatedatetag_dht22_%s.log" % dateTag, level=logging.INFO)

handler = logging.handlers.TimedRotatingFileHandler("/tmp/temploggerrotatedatetag_dht22.log", backupCount=366)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

handler.setFormatter(formatter)

logger.addHandler(handler)

#https://stackoverflow.com/questions/31919905/help-with-creating-temperature-humidity-script
#20200103 19u30 addedscript with logging with aid of above webpage

#20200103 19u58 added timestamp
import os
os.system("date +'%H:%M:%S'")

import time
import Adafruit_DHT

#20200103 19u33 edit your home folder name + log file name + path
filepath = '/home/your-user-name/temploggerdht22test.log'

#20221209 15u28 Pin # according to adafruit NOT gpio #
pin = 12

sensor = Adafruit_DHT.DHT22

#20221209 17u08 adapted to show 2 decimal digits
while True:
    # get current time
    sampletime = time.localtime()
    # sample sensor values
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    # when script run in terminal will show data to verify if read was succesful
    print("Temperature={0:0.2f}*C  Humidity={1:0.2f}%".format(temperature, humidity))
    humidity2 = '{0:0.2f}'.format(humidity)
    temperature2 = '{0:0.2f}'.format(temperature)
    
    time.sleep(2)
    
    # write data to log
    datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    logger.info(' %s , RPi Temp DHT22Sensor in C: %s, Humidity:, %s', datetimeWrite, temperature2, humidity2)
    # when script run in terminal will show data writen to log file
    print (temperature2,"'C", humidity2,"'%")

    break
