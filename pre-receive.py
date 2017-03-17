#! /usr/bin/python2.7
"""

	Simple python script for push notifications. Notifications ...

	Author: Hrvoje Novosel<hrvojedotnovosel@gmail.com>
	Created: 17. Mar 2017

"""

import sys
import os
import json
import subprocess

DEBUG = True
# path to config file contaning information on target email addresses, servers, ...
CONFIG_FILE = './../config.json'


def Log(message):
	"""
		Message logging function
	"""
	print("Push notification: {}".format(message))


def run_command(command, panic=False, nlines=None):
	"""
		Runs command and returns last output line
		If panic return value of the command must be 0
	"""
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	retval = p.stdout.readlines()
	if p.wait() != 0 and panic:
		Log('Cannot get extract repository info, exiting ...')
		return ''

	return retval.pop()


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


def main():
	"""
		Perform the stuff
	"""
	# check for basic git info first
	git_dir = run_command('git rev-parse --git-dir', True).strip()
	git_project = repo_details(git_dir, 'project')

	print git_project

	conf = get_configuration()
	if conf is None:
		Log('Valid configuration missing')
		return

	# print(conf)
	# check for modified files

	# msg and file diff, see what to do with that


if __name__ == '__main__':
	"""
		TODO: utilize debug/prod env
	"""
	print sys.argv
	main()