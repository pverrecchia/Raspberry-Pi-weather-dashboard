#!/usr/bin/env python

#This script polls the BME280 weather sensor and writes the sensor data to a MySQL database
#It can be configured in crontab to run every 5 minutes

import MySQLdb
import time
from time import strftime
from Adafruit_BME280 import *

#Setup database
db = MySQLdb.connect(host="localhost", user="root",passwd="password", db="rpi_database")
cur = db.cursor()

#Initialize BME280 atmospheric sensor
bme = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)


while True:
    #Poll sensor and record data
    datetime = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    temp = round(bme.read_temperature(), 2)
    pressure = round((bme.read_pressure() / 100),2) #divide reading by 100 for hectopascals (hPa)
    humidity = round(bme.read_humidity(), 2)

    sql = ("INSERT INTO weather_data (dateTime, temperature, pressure, humidity) VALUES (%s,%s,%s,%s)",(datetime, temp, pressure, humidity))

    try:
        # Insert and commit data to database
        cur.execute(*sql)
        db.commit()

    except:
        # Rollback in case there is any error
        db.rollback()
        print "Failed writing to database"
               
    cur.close()
    db.close()
    break
