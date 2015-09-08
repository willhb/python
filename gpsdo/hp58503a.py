#!/usr/bin/python
# hp58503a.py HP 58503A Driver
# Todo: Error handling and recovery: Bad things happen if the serial interace gets out of sync.
# 		Additional functionality support: Current functionality is only useful to log operating parameters once output is valid.
#		Handle serial port processing better.
#		
#		Overall: Work in progress!!

import serial

#strip newlines and carriage return if present
def process_serial(a):
	alen = len(a)
	if alen > 0:
		if a[alen-1] == '\n':
			if a[alen-2] == '\r':
				return a[0:alen-2]
			else:
				return a[0:alen-1]
		else:
			return a
	else:
		return a
	

class hp58503a:

	def __init__(self):
		# Add option to set serial port and parameters
		self.serport = serial.Serial('/dev/ttyUSB0', 19200, timeout=1)

	def close(self):
		self.serport.close()

	def open(self):
		self.serport.open()

	def cls(self):
		self.serport.write("*CLS\n".encode())
		recv_response = self.serport.readline()
		recv_response = self.serport.readline()
		return process_serial(recv_response)

	def idn(self):
		self.serport.write("*IDN?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return process_serial(recv_response)

	def ref_valid(self):
		self.serport.write(":GPS:REF:VAL?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = process_serial(self.serport.readline())
		if recv_response == '1':
			return True
		else:
			return False

	def alarm(self):
		self.serport.write(":LED:ALARM?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = process_serial(self.serport.readline())
		if recv_response == '1':
			return True
		else:
			return False

	def gpslock(self):
		self.serport.write(":LED:GPSLOCK?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = process_serial(self.serport.readline())
		if recv_response == '1':
			return True
		else:
			return False

	def holdover(self):
		self.serport.write(":LED:HOLDOVER?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = process_serial(self.serport.readline())
		if recv_response == '1':
			return True
		else:
			return False

	def gpscount(self):
		self.serport.write(":GPS:SATELLITE:TRACKING:COUNT?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return process_serial(recv_response)

	def syncstate(self):
		self.serport.write(":SYNC:STATE?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return process_serial(recv_response)

	def efcrel(self):
		self.serport.write(":DIAG:ROSC:EFC:REL?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return process_serial(recv_response)

	def efcabs(self):
		self.serport.write(":DIAG:ROSC:EFC:ABS?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return process_serial(recv_response)

	def time(self):
		self.serport.write(":PTIME:TIME?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return process_serial(recv_response)

	def date(self):
		self.serport.write(":PTIME:DATE?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return process_serial(recv_response)

	def tint(self):
		self.serport.write(":SYNC:TINT?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return float(process_serial(recv_response))

	def tfom(self):
		self.serport.write(":SYNC:TFOM?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return int(process_serial(recv_response))

	def ffom(self):
		self.serport.write(":SYNC:FFOM?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return int(process_serial(recv_response))

	def leap_acc(self):
		self.serport.write(":PTIM:LEAP:ACC?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return int(process_serial(recv_response))

	def holdoverquality(self):
		self.serport.write(":SYNC:HOLD:TUNC:PRED?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return process_serial(recv_response)

	def error(self):
		self.serport.write("SYSTEM:ERROR?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return process_serial(recv_response)

	def lifetime(self):
		self.serport.write("DIAG:LIF:COUN?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		return int(process_serial(recv_response))

	def survey_progress(self):
		self.serport.write("GPS:POS:SURV:PROG?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = self.serport.readline()
		if recv_response[:5] == "E-221":
			return 100.0
		else:
			return float(process_serial(recv_response))

	def location(self):
		self.serport.write("GPS:POS?\n".encode())
		self.serport.flush()
		sent_cmd = self.serport.readline()
		recv_response = process_serial(self.serport.readline())
		r = recv_response.split(",")
		return (r[0],int(r[1]),int(r[2]),float(r[3]),r[4],int(r[5]),int(r[6]),float(r[7]),float(r[8]))

	def status(self):
		self.serport.write("SYSTEM:STATUS?\n".encode())
		self.serport.flush()
		send_cmd = self.serport.readline()
		recv_response=[]
		for linecount in range(0,24):
			recv_response.append(process_serial(self.serport.readline()))
		return recv_response

	def pretty_status(self, status_message):
		for count in range (0,24):
			print status_message[count]

# Need to check if all the data on the status page is available elsewhere
# currently I don't believe satellite signal strength is available, must
# parse out of the slow status screen. Might as well grab everything well
# we are at it. 

	def get_sats(self, status_message=None):
		if status_message is None:
			status_message = self.status()
		tracked = []
		untracked = []

		a = status_message

		gps_tracking = int(a[11].split(": ")[1].split(" _")[0])
		gps_not_tracking = int(a[11].split(": ")[2].split(" _")[0])

		for count in range (13,13+gps_tracking):
			tracked.append((int(a[count].split()[0]), int(a[count].split()[1]),int(a[count].split()[2]),int(a[count].split()[3])))

		for count in range (13,13+gps_not_tracking):

			b = a[count].split()

			if count > 12+gps_tracking:
				if b[0] == "*" and len(b[0]) == 1:
					b[0] = b[0]+b[1]
					b[1] = b[2]
					b[2] = b[3]

				if b[1] == "Acq":
					untracked.append((b[0], 0,0,-1))
				elif b[1][0] == "-":
					untracked.append((b[0], 0,0,-2))
				else:
					untracked.append((b[0], int(b[1]),int(b[2]),0))
			else:
				if b[4] == "*" and len(b[4]) == 1:
					b[4] = b[4]+b[5]
					b[5] = b[6]
					b[6] = b[7]

				if b[5] == "Acq":
					untracked.append((b[4], 0,0,-1))
				elif b[5][0] == "-":
					untracked.append((b[4], 0,0,-2))
				else:
					untracked.append((b[4], int(b[5]),int(b[6]),0))

			if untracked[count-13][0][0] == '*':
				attempted_track = list(untracked[count-13])
				attempted_track[0] = int(attempted_track[0][1:])
				attempted_track[3] = attempted_track[3] | 4
				untracked[count-13] = tuple(attempted_track)
			else:
				attempted_track = list(untracked[count-13])
				attempted_track[0] = int(attempted_track[0])
				untracked[count-13] = tuple(attempted_track)

		return (gps_tracking, tracked, gps_not_tracking, untracked)
			
		
