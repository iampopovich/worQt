import os
import math
import datetime

def set_file_error(self):
	date = datetime.now().isoformat()
	login = os.login()
	file_error = '{}_{}_error.log'.format(date, login)
	if os.path.exists(file_error):
		self.file_error = file_error
	else:
		file = create_file_error()
		self.file_error = file

def set_file_log(self):
	date = datetime.now().isoformat()
	login = os.login()
	file_log = '{}_{}.log'.format(date,login)
	if os.path.exists(file_log):
		self.file_log = file_log 
	else:
		file = create_file_log()
		self.file_error = file

def create_file_log():
	date = datetime.now().isoformat()
	login = os.login()
	file_log = '{}_{}.log'.format(date,login)
	with open('{}_{}.log','a') as out_log:
		out_log.close()
	return file_log

def create_file_error():
	date = datetime.now().isoformat()
	login = os.login()
	file_error = '{}_{}_error.log'.format(date, login)
	with open(file_error,'a') as out_error:
		out_error.close()
	return file_error

def get_file_log():
	pass

def get_file_error():
	pass

def log_dump_crash():
	pass

def log_write_action():
	pass