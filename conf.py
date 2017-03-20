"""
	Configuration script for sharing single configuration among multiple scripts

"""

DEBUG = True
# path to config file contaning information on target email addresses, servers, ...
CONFIG_FILE = './../config.json'

import os
import sys
import json
import subprocess

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


def read_commits():
	"""
		Generator function of commits from std in
	"""
	for ln in sys.stdin:
		args = ln.split(' ')
		if len(args) == 3:
			yield args
		else:
			yield None


# a set of helper functions
def Log(message):
	"""
		Message logging function
	"""
	print("Push notification: {}".format(message))


def run_command(command, panic=False, nlines=1):
	"""
		Runs command and returns last output line
		If panic return value of the command must be 0
	"""
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	retval = p.stdout.readlines()
	if p.wait() != 0 and panic:
		Log('Cannot get extract repository info, exiting ...')
		sys.extit()

	if nlines == 1:
		return retval.pop()
	else:
		if nlines == 'max':
			nln = len(retval)
		else:
			nln = min(len(retval), nlines)
		retstr = ""
		for i in range(nln):
			retstr += retval[i]

		return retstr


def repo_details(git_path, property):
	"""
		Reads git description fp and returns basic info on git repository
	"""
	fname = git_path + '/'
	if property == 'project':
		fname += 'description'

	if os.path.isfile(fname):
		with open(fname, 'r') as fp:
			return fp.read()
	else:
		return 'undefined'