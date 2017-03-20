#! /usr/bin/python2.7
"""

	Simple hook for sending server push summary notification message

	Line for stdin (test example):
	fc88f2f47129347ee20f73632927e84dae67c4f7 1de59c8239ea271a9cb52e8b6a7b50d3939207b3 refs/heads/master
	<old-value> SP <new-value> SP <ref-name> LF

	can be tested with test line file:
	./post-receive.py < test_line

	Author: Hrvoje Novosel<hrvojedotnovosel@gmail.com>
	Created: 17. Mar 2017

"""

import conf

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
	Log = conf.Log
	# check for basic git info first
	git_dir = conf.run_command('git rev-parse --git-dir', True).strip()
	git_project = 'Project ' + conf.repo_details(git_dir, 'project')

	cfg = conf.get_configuration()
	if cfg is None:
		Log('Valid configuration missing')
		return

	msg = ''
	# check for modified files
	for args in conf.read_commits():
		if not args is None:
			git_project += ' branch: ' + args[2][args[2].rfind('/')+1:]
			commit = conf.run_command(' git log -n1 --format="%an<%ae> %s" ' + args[1] + ' ' + args[2])
			diff   = conf.run_command('git diff --stat {} {} {}'.format(args[1], args[0], args[2]), False, 'max')
	
			# TODO: if set in config, zip detailes line diff
			msg += "Commit:\n{}\nDiff:\n{}\n\n".format(commit, diff)

	# send a message to all recipients
	if not cfg['server'] is None:
		for r in cfg['recipient_lst']:
			send_message(r, git_project, msg, cfg['server'])


if __name__ == '__main__':
	"""
		Scripts entry point
	"""
	main()