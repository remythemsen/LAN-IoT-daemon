#!/usr/bin/env python3
# This script contains the datamanagement functionality of the application
import sqlite

#run sql script setting up db if the db 'main.db' does not exist
def setup_db(): 
	raise NotImplementedError

#persist a new device to the database
def add_device(device_in_JSON): 
	#open connection
	#check if device already exists
	#insert
	raise NotImplementedError

#remove persisted device from db
def remove_device(device_mac):
	raise NotImplementedError

def db_connection():
	conn = sqlite3.connect('./main.db')
	return conn

#logs select devices state
def log_state():
	raise NotImplementedError

#fetches all devices with settings associated with a specific profile
def get_profile():
	try:
		table_name = "profiles"
		# Getting associated devices and their settings from DB

		conn = db_connection()
		conn.row_factory = dict_factory
		c = conn.cursor()
		c.execute('''
								SELECT devices.id, devices.mac, devices.ip, types.name AS device_type, settings.setting
								FROM settings
								INNER JOIN devices ON settings.device = devices.id
								INNER JOIN types ON devices.type = types.id
								WHERE profile = (SELECT id FROM profiles WHERE name = ?)''',(profile,))

		all_rows = c.fetchall()
		# JSON format results
		print(json.dumps(all_rows))
	except:
		raise
	finally:
		conn.close()


def dict_factory(cursor, row):
	rowDict = {}
	for idx, col in enumerate(cursor.description):
		if(col[0] == "setting"):
			# Convert string setting to json object
			json_dic = json.loads(row[idx])
			rowDict.update(json_dic)
		else:
			rowDict[col[0]] = row[idx]
	return rowDict

def help():
	return ""

operation = sys.argv[1].lower()
if(operation == "add"):
	raise NotImplementedError

elif(operation == "remove"):
	raise NotImplementedError

elif(operation == "profile"):
	raise NotImplementedError

elif(operation == "log"):
	raise NotImplementedError
	
elif(operation == "help"):
	print(help_message())
else:
	print("Unknown parameter: "+str(operation))
	print("Try help for more information")
