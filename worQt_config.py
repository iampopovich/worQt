import json
import os


def get_config():
    try:
        file_config = get_config_file()
        with open(file_config) as config:
            parsed_file = json.load(config)
    except:
        file_config = create_file_config()
        with open(file_config) as config:
            parsed_file = json.load(config)
    finally:
        return json.dumps(parsed_file, indent=4)


def set_config(config):
    file_config = get_config_file()
    with open(file_config) as out_config:
        json.dump(config, out_config)


def create_file_config():
    file_config = 'config.cfg'
    config = {
        'host': '',
        'port': '',
        'user': '',
        'password': '',
        'reciever': ''
    }
    with open(file_config, 'w') as out_config:
        json.dump(config, out_config)
    return file_config


def get_config_file():
    file_config = 'config.cfg'
    return file_config if os.path.exists(file_config) else create_file_config()
