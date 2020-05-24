import json
import os

def get_config():
	file_config = get_config_file()
	with open(file_config) as config:
		parsed_file = json.load(config)
	return parsed_file

def set_config(config):
	file_config = get_config_file()
	with open(file_config) as out_config:
		json.dump(config,out_config)

def create_file_config():
	file_config = 'config.cfg'
	with open(file_config,'a') as out_config:
		out_config.close()
	return file_config

def get_config_file():
	file_config = 'config.cfg'
	return file_config if os.path.exists(file_config) else create_file_config()