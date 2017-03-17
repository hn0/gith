#! /usr/bin/python2.7
"""

	Simple python script for push notifications. Notifications ...

	Line for stdin (test example):
	fc88f2f47129347ee20f73632927e84dae67c4f7 1de59c8239ea271a9cb52e8b6a7b50d3939207b3 refs/heads/master
	<old-value> SP <new-value> SP <ref-name> LF

	can be tested with test line file:
	./post-receive.py < test_line

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


def send_message(recipient, title, message, server):
	"""
		Sends a message to each recipient from the list
	"""
	# print(server)
	print(title)
	print(message)


def main():
	"""
		Perform the stuff
	"""
	# check for basic git info first
	git_dir = run_command('git rev-parse --git-dir', True).strip()
	git_project = 'Project ' + repo_details(git_dir, 'project')

	conf = get_configuration()
	if conf is None:
		Log('Valid configuration missing')
		return

	msg = ''
	# check for modified files
	for ln in sys.stdin:
		args = ln.split(' ')
		if len(args) == 3:
			git_project += ' branch: ' + args[2][args[2].rfind('/')+1:]
			commit = run_command(' git log -n1 --format="%an<%ae> %s" ' + args[1] + ' ' + args[2])
			diff   = run_command('git diff --stat {} {} {}'.format(args[1], args[0], args[2]), False, 'max')

			# TODO: see if summary of changes will be needed?
			msg += "Commit:\n{}\nDiff:\n{}\n\n".format(commit, diff)

	# send a message to all recipients
	if not conf['server'] is None:
		for r in conf['recipient_lst']:
			send_message(r, git_project, msg, conf['server'])


if __name__ == '__main__':
	"""
		TODO: utilize debug/prod env
	"""
	main()