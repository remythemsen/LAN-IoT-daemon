#!/usr/bin/env python3
import os
import sys
# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)

import json
from lifxlan import LifxLAN
from lifxlan import Light

class TPPlugBridge():
	def apply(self, settings):
		pass
	
	def state(self, device_ref):
		pass


class LifxBridge():
	def	apply(self, device_profile):
		duration = device_profile['duration']												#milliseconds
		dev = Light(device_profile['mac'],device_profile['ip'])
		dev.set_power(device_profile['power'], duration) 						#range [0,65535]
		dev.set_hue(device_profile['hue'], duration) 								#range [0-65535]
		dev.set_saturation(device_profile['saturation'], duration)	#range [0-65535]
		dev.set_brightness(device_profile['brightness'], duration) 	#range [0-65535]
		dev.set_colortemp(device_profile['temperature'], duration) 	#range [2500-9000]
	
	def state(self, device):
		bulbRef = Light(device['mac'],device['ip'])
		hsbk = bulbRef.get_color()
		dev = Device(device['mac'],device['ip'],bulbRef.get_power(),hsbk[0],hsbk[1],hsbk[2],hsbk[3])

		return json.dumps(dev.__dict__)


class Device(object):
	def __init__(self, mac, ip, power, hue, saturation, brightness, temperature):
		self.mac = mac
		self.ip = ip
		self.power = power
		self.hue = hue
		self.saturation = saturation
		self.brightness = brightness
		self.temperature = temperature
		
def selectBridge(x):
	switcher = {
		"bulb": LifxBridge(),
		"plug": TPPlugBridge()
	}
	return switcher.get(x.lower(), "Unknown bridge was provided.")


def help_message():
	return "parameters are of the form:\nprogram.py state|apply [json formatted profile]"

def get_states(json_formatted_devices):
	#Read state from each device in jsonString, return json formatted string
	result = '['
	if not json_formatted_devices.strip():
		raise Exception("You need to provide a JSON formatted device list, empty string was found.")
	
	device_list = json.loads(json_formatted_devices)
	if(len(device_list) == 0):
		return result + ']'	
	else:
		for device in device_list[:-1]:
			bridge = selectBridge(device['device_type']) 
			# Action
			try:
				result += bridge.state(device) + ','
			except:
				continue #TODO log this occurrence

		try:
			last_device = device_list[len(device_list-1)]
			bridge = selectBridge(last_device['device_type'])
			result += bridge.state(last_device)
		except:
			pass #TODO log this occurrence

		return result + ']'	

def apply_settings(json_formatted_device_settings):
	
	if not json_formatted_device_settings.strip():
		raise Exception("You need to provide a JSON formatted device list, empty string was found.")
	
	device_list = json.loads(json_formatted_device_settings)
	if(len(device_list) == 0):
		raise Exception("Empty device list was provided")	
	else:
		for setting in device_list:
			bridge = selectBridge(setting['device_type']) 
			# Action
			try:
				bridge.apply(setting)
			except:
				continue #TODO log this occurence
	

operation = sys.argv[1]
if(operation.lower() == "state"):
	print(get_states(sys.stdin.read()))
elif(operation == "apply"):
	apply_settings(sys.stdin.read())
elif(operation == "help"):
		print(help_message())
else:
	print("Unknown parameter: "+str(operation))
	print("Try help for more information")


