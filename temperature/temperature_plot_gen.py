# temperature_plot_gen.py
# Generate a temperature and pressure plot from values stored to a postgresql database
# Todo: Clean up plotting

# Standard python libraries
import datetime
import time
import math

# PostgreSQL database management
import psycopg2

# Data manipulation and plotting
from pylab import *
from numpy import arange
from matplotlib import *
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

# Convert Celsius to Fahrenheit
def ctof(temp):
	return temp*(9.0/5.0) + 32.0

# Todo: configurable plot time
# 1/2 day into 10 second segments
limit = 8640/2 

# Altitude used for station pressure to sealevel pressure
# Data from HP 58503A GPS survey
altitude = 101.90

# Don't use real passwords for github commits :)
conn = psycopg2.connect("dbname='temperature' user='test' host='10.0.1.233' password='test'")
cur = conn.cursor()

while True:

	cur.execute("SELECT * FROM sensors ORDER BY index_id DESC LIMIT (%s)", [limit])
	data = cur.fetchall()

	timestamp = []
	temperature = []
	pressure = []
	
	# Todo: Better way to get updated data without downloading everything? 
	for i in range (0, len(data)):
		timestamp.append(data[i][6])
		temperature.append(data[i][3])
		# Station to sealevel conversion from http://www.sandhurstweather.org.uk/barometric.pdf
		pressure.append((data[i][4])/(math.exp((-altitude)/((temperature[i]+273.15)*29.263)))/100.0)
		# Convert to Fahrenheit for display
		temperature[i] = ctof(temperature[i])

	fig, ax1 = plt.subplots()
	ax1.plot(timestamp,temperature)
	
	# Calculate plot time shown
	ax1.set_xlabel('Time - Previous ' + str(len(data)/6/60) + ' hours and ' + str( len(data)/6 - (len(data)/6/60 * 60)) + " minutes")
	ax1.set_ylabel('Temperature (F)', color='blue')

	ax2 = ax1.twinx()
	ax2.plot(timestamp,pressure,'red')
	ax2.set_titlelabel('Pressure (mbar)', color='red')

	ax1.set_title("Current Temperature:" + "{0:.1f} F, ".format(temperature[0]) + "Current Pressure: " + "{0:.2f} mbar".format(pressure[0]))

	ax1.set_xlim( timestamp[0], timestamp[-1] )

	ax1.set_ylim( min(temperature)-5, max(temperature)+10)
	ax2.set_ylim( min(pressure)-10, max(pressure)+5)

	ax1.xaxis.set_major_locator( HourLocator() )
	ax1.xaxis.set_minor_locator( MinuteLocator() )
	ax1.xaxis.set_major_formatter( DateFormatter('%H:%M') )
	ax1.invert_xaxis()

	ax1.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
	fig.autofmt_xdate()
	fig.set_size_inches(15,5)
	
	# Push to the webserver
	savefig('/var/www/html/temperature.png')
	
	# Clear and close the figure
	clf()
	close()
	
	# Temperature database only updates every 10 seconds
	time.sleep(10)

conn.close()
