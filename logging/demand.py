import RainEagle
import time
import socket
import requests


raineagle = RainEagle.Eagle(debug=0, addr="10.0.1.191", username="0021dc", password="8307add1c7a04510")
last_power = 0

while True:
	time.sleep(10)
	try:
		demand = raineagle.get_usage_data()[u'demand']
	except:
		print("Could not collect data")

	try:
		power = str(int(float(demand)*1000))
		last_power = power
	except:
		power = last_power

	data = 'power,host=viatiempo value=' + power
	try:
		res = requests.post(url='http://10.0.1.194:8186/write', data=data)
	except:
		print("Could not post data")	

	
