#!/usr/bin/env python3
import os
import sys
import sqlite3
import json

# This script is meant to be called regulary by a cron job
profile = sys.argv[1]


# get sample input from stdin, fetch a profile, and activate it

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

# Connect with persistent data layer
try:
	table_name = "profiles"
	# Getting associated devices and their settings from DB

	conn = sqlite3.connect('./test.db')
	conn.row_factory = dict_factory
	c = conn.cursor()

	c.execute('''SELECT devices.id, devices.mac, devices.ip, types.name AS device_type, settings.setting
		FROM settings
		INNER JOIN devices ON settings.device = devices.id
		INNER JOIN types ON devices.type = types.id
		WHERE profile = (SELECT id FROM profiles WHERE name = ?)''',(profile,))

	all_rows = c.fetchall()
	# JSON format results
	print(json.dumps(all_rows))
except:
	print("db connection failed")
	raise
finally:
	conn.close()

