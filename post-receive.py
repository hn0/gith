#! /usr/bin/python2.7
"""
	
	Post receive message handler

	Line for stdin (test example):
	fc88f2f47129347ee20f73632927e84dae67c4f7 1de59c8239ea271a9cb52e8b6a7b50d3939207b3 refs/heads/master
	<old-value> SP <new-value> SP <ref-name> LF

	can be tested with test line file:
	./post-receive.py < test_line

	Author: Hrvoje Novosel<hrvojedotnovosel@gmail.com>
	Created: 17. Mar 2017

"""

import conf
import summary_msg as emsg


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
			msg += emsg.read_commit(args[0], args[1], args[2])

	# send a message to all recipients
	if not cfg['server'] is None:
		for r in cfg['recipient_lst']:
			# res = send_message(r, git_project, msg, cfg['server'])
			res = emsg.send_message(r, git_project, msg, cfg['server'])
			if not res is None:
				Log(res)


if __name__ == '__main__':
	"""
		Scripts entry point
	"""
	main()