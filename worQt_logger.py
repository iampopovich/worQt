import os
import worQt_timer
import json

def set_file_error(self, file_error):
	self.file_error = file_error

def set_file_log(self, file_log):
	self.file_log = file_log 

def create_file_log():
	date = worQt_timer.get_today().isoformat()
	login = os.login()
	file_log = '{}_{}.log'.format(date,login)
	with open('{}_{}.log','a') as out_log:
		out_log.close()
	return file_log

def create_file_error():
	date = worQt_timer.get_today().isoformat()
	login = os.login()
	file_error = '{}_{}_error.log'.format(date, login)
	with open(file_error,'a') as out_error:
		out_error.close()
	return file_error

def get_file_log():
	date = worQt_timer.get_today().isoformat()
	login = os.login()
	file_log = '{}_{}.log'.format(date,login)
	return file_log if os.path.exists(file) else create_file_log()

def get_file_error():
	date = worQt_timer.get_today().isoformat()
	login = os.login()
	file_log = '{}_{}_error.log'.format(date,login)
	return file_log if os.path.exists(file) else create_file_error()
	

def log_dump_crash():
	pass

def log_write_action():
	pass