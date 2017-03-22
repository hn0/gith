"""

	Simple email notification script, sends summary of push on the server side to predefined list of recipients

"""


import conf
import smtplib
from email.mime.text import MIMEText

# TODO: init the object with project info


def read_commit(old_id, new_id, branch):
	"""
		Reads comment and returns summary message		
	"""
	commit = conf.run_command(' git log -n1 --format="%an<%ae> %s" ' + new_id + ' ' + old_id)
	diff   = conf.run_command('git diff --stat {} {} {}'.format(new_id, old_id, branch), False, 'max')

	# TODO: if set in config, zip detailes line diff
	return "Commit:\n{}\nDiff:\n{}\n\n".format(commit, diff)


def send_message(recipient, title, message, server):
	"""
		Sends a message to each recipient from the list
	"""
	# print(server)
	# print(title)
	# print(message)

	try:
		msg = MIMEText(message)
		msg['From']    = server['user']
		msg['Subject'] = title
		msg['To']      = recipient

		# current support is just for plain smtp server, ssl support in plan
		s = smtplib.SMTP(server['host'])
		s.ehlo_or_helo_if_needed()
		if not s is None:
			s.login(server['user'], server['pwd'])
			if not conf.DEBUG:
				s.sendmail(server['user'], recipient, msg.as_string())
				return None
			else:
				return "\nSending the message:" + msg.as_string()
				
	except Exception as ex:
		return 'Message has not been sent: {}'.format(str(ex))