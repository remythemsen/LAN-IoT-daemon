import os
import sys
import sqlite3

# This script is meant to be called regulary by a cron job

# Connect with persistent data layer

try:

	conn = sqlite.connect('test.db')

	c.execute('SELECT * FROM {tn}'.\
					format(tn=table_name))

	all_rows = c.fetchall()
	print('1):', all_rows)
except:
	return
finally:
	conn.close()

