"""
	Configuration script for sharing single configuration among multiple scripts

"""

# path to config file contaning information on target email addresses, servers, ...
CONFIG_FILE = './../config.json'

import os
import json

def get_configuration():
	"""
		Reads and pases configuration file in JSON format
	"""
	if os.path.isfile(CONFIG_FILE):
		with open(CONFIG_FILE, 	'r') as fp:
			return json.loads(fp.read())
	else:
		Log('Configuration file not present on the system')

	return None