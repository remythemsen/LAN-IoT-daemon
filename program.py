import os
import sys
# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)

import json
from lifxlan import LifxLAN
from lifxlan import Light


class Device(object):
	def __init__(self, mac, ip, power, hue, saturation, brightness, temperature):
		self.mac = mac
		self.ip = ip
		self.power = power
		self.brightness = brightness
		self.hue = hue
		self.saturation = saturation
		self.temperature = temperature
		

def help_message():
	return "parameters are of the form:\nprogram.py state|apply [json formatted profile]"
# Takes 'profile' in json stdin

#stdin
operation = sys.argv[1]
if(operation == "state"):
	print("Getting state")
	#Read state from each device in jsonString, return json formatted string
	
	# Parse 
	jsonString = sys.argv[2]
	jObject = json.loads(jsonString)

	devices_in_JSON = []
	for device in jObject['devices']:
		try:
			bulbRef = Light(device['mac'],device['ip'])
			hsbk = bulbRef.get_color()
			dev = Device(device['mac'],device['ip'],bulbRef.get_power(),hsbk[0],hsbk[1],hsbk[2],hsbk[3])
			devices_in_JSON.append(json.dumps(dev.__dict__))
		except:
			continue

	result = ""
	if(len(devices_in_JSON) > 0):
		result = '{"devices":[' + devices_in_JSON[0] 

		for i in range(1, len(devices_in_JSON)):
			result += ',' + devices_in_JSON[i] 

		result += ']}'
	else:
		result = '{"devices":[]}'

	print(result)
	
elif(operation == "apply"):
	# Parse 
	jsonString = sys.argv[2]
	jObject = json.loads(jsonString)

	
	# Action
	for device_profile in jObject['devices']:
		duration = device_profile['duration']												#milliseconds
		dev = Light(device_profile['mac'],device_profile['ip'])
		dev.set_power(device_profile['power'], duration) 						#range [0,65535]
		dev.set_brightness(device_profile['brightness'], duration) 	#range [0-65535]
		dev.set_hue(device_profile['hue'], duration) 								#range [0-65535]
		dev.set_saturation(device_profile['saturation'], duration)	#range [0-65535]
		dev.set_colortemp(device_profile['temperature'], duration) 	#range [2500-9000]

		print("profile applied for: "+dev.get_label())

elif(operation == "help"):
	print(help_message())
else:
	print("Unknown parameter: "+str(operation))
	print("Try help for more information")


