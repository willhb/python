# bmp180_data_collect.py
# Collect temperature and pressure from the Bosch BMP180 sensor and store to a postgresql database
# Requires psycopg2 for PostgreSQL and the Adafruit_BMP library for interfacing with the BMP180. 
# Runs on the Bealgebone Black

import datetime
import time
import psycopg2
import Adafruit_BMP.BMP085 as BMP085

#wait time to collect data
sleeptime = 10

#database is populated with these items for later use
sensor_name = "Beaglebone BMP180"
sensor_id = 0

#don't commit real passwords to github :) 
conn = psycopg2.connect("dbname='temperature' user='test' host='10.0.1.233' password='test'")
cur = conn.cursor()

sensor = BMP085.BMP085()

#todo: error handling...
while True:
	cur.execute("INSERT INTO sensors (sensor_id, sensor_name, temperature,pressure, timestamp) VALUES (%s, %s, %s, %s, %s)", (sensor_id, sensor_name, sensor.read_temperature(), sensor.read_pressure(), datetime.datetime.utcnow()))
	conn.commit()
	time.sleep(sleeptime)
