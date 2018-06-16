import configparser
import os

DEFAULT_NAME = 'config.ini'

def create_config(path=None):
    config = configparser.ConfigParser()
    config.add_section("settings")
    config.set("settings","path_to_log", "None")
    config.set("settings", "path_to_db", "None")
    if path is None:
        path = DEFAULT_NAME
    else:
        path.os.path.join(path, DEFAULT_NAME)
    with open(path, 'w') as config_file:
        config.write(config_file)

def load_config(path=None):
    config = configparser.ConfigParser
    if path is None:
        path = DEFAULT_NAME
    else:
        path.os.path.join(path, DEFAULT_NAME)
    if not os.path.exists(path):
        raise NotImplementedError
    config.read(None,path)
    return config

def get_path_to_db(path=None):
    config = load_config(path)
    path_to_db = config.get("settings","path_to_db")
    if path_to_db == 'None':
        path_to_db = os.path.join('~/','Tracker_DB')
    return path_to_db

def get_path_to_log(path=None):
    config = load_config(path)
    path_to_log = config.get('settings','path_to_db')
    if path_to_log == 'None':
        path_to_db = os.path.join('~/', 'Tracker/logger.log')