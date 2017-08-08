import time
import socket
import requests
import json
import subprocess

proc = subprocess.Popen(['rtl_433','-Fjson','-q','-R 40'],stdout=subprocess.PIPE)

last_time = 0
raincounter = 0
rain_accumulation = 0
battery = 0
sensor_id = 0
id = 0
channel = 0
type = 0
temp = 0
humidity = 0

while True:
	try:
		data = proc.stdout.readline()
	except:
		print " "

	if data[0] == "{":
		line = json.loads(data)
		model = line[u'model']
		time = line[u'time']
		if model == "Acurite 5n1 sensor":
			raincounter = line[u'raincounter_raw']
			rain_accumulation = line[u'rainfall_accumulation']
			battery = line[u'battery']
			sensor_id = line[u'sensor_id']
			channel = line[u'channel']
		if model == "Acurite tower sensor":
			sensor_id = line[u'id']
			channel = line[u'channel']
			battery = line[u'battery']
			humidity = line[u'humidity']
			temp = line[u'temperature_C']

	if (time != last_time):
		last_time = time
		post = 0

		if model == "Acurite 5n1 sensor":
			if battery == "OK":
				battery = 0
			else:
				battery = 1
			data = 'rain,host=viatiempo raincounter='+str(raincounter)+',accumulation='+str(rain_accumulation)+',battery='+str(battery)
			post = 1
		
		if model == "Acurite tower sensor":
			data = 'temp_'+str(channel)+',host=viatiempo temperature='+str(temp)+',humidity='+str(humidity)+',battery='+str(battery)
			post = 1
		
		if post == 1:
			try:
				res = requests.post(url='http://10.0.1.194:8186/write', data=data)
			except:
				print("Could not post data")	

	
