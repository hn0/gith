#! /usr/bin/python2.7
"""

	Simple python script for push notifications. Notifications ...

	Author: Hrvoje Novosel<hrvojedotnovosel@gmail.com>
	Created: 17. Mar 2017

"""

import os
import sys
import json


# path to config file contaning information on target email addresses, servers, ...
CONFIG_FILE = './../config.json'


def Log(message):
	"""
		Message logging function
	"""
	print("Push notification: {}".format(message))


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


def main():
	"""
		Perform the stuff
	"""
	conf = get_configuration()
	if conf is None:
		Log('Valid configuration missing')
		return

	print(conf)
	# check for modified files

	# msg and file diff, see what to do with that


if __name__ == '__main__':
	print sys.argv
	main()