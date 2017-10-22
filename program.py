import os
import sys
import json

# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)

from lifxlan import LifxLAN
from lifxlan import Light

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

	for device in jObject['devices']:
		dev = Light(device['mac'],device['ip'])
		print(dev.get_label() + " " + str(dev.get_power()))
	
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


