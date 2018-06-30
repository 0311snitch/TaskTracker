import configparser
import os

import sys

DEFAULT_NAME = 'config'
HOME = os.environ['HOME']

DEFAULT = 'config'
DEFAULT_PATH = os.path.join(HOME, DEFAULT)


def create_config(db_path='None', log_path='None', path_to_test_db='None'):
    config = configparser.ConfigParser()
    config.add_section("settings")
    config.set('settings', 'path_to_log', log_path)
    config.set('settings', 'path_to_db', db_path)
    config.set('settings', 'path_to_test_db', path_to_test_db)

    path = os.path.dirname(os.path.abspath(__file__))
    path = path[:-7]
    path = os.path.join(path, DEFAULT_NAME)
    check_tracker_folder(path)
    path = os.path.join(path, 'conf.ini')

    with open(path, 'w') as config_file:
        config.write(config_file)


def load_config():
    config = configparser.ConfigParser()
    path = os.path.dirname(os.path.abspath(__file__))
    path = path[:-7]
    path = os.path.join(path, DEFAULT_NAME)

    if not os.path.exists(path):
        create_config()
    path = os.path.join(path, 'conf.ini')
    config.read(path)
    return config


def get_path_to_db():
    config = load_config()
    path_to_db = config.get('settings', 'path_to_db')
    if path_to_db == 'None':
        path = os.path.dirname(os.path.abspath(__file__))
        path = path[:-7]
        path_to_db = os.path.join(path, 'database.sqlite3')
        print(path_to_db)
    return path_to_db


def get_path_to_test_db():
    config = load_config()
    path_to_test_db = config.get('settings', 'path_to_test_db')
    if path_to_test_db == 'None':
        path_to_test_db = os.path.join(HOME, 'Takinata')
    return path_to_test_db


def get_path_to_log():
    config = load_config()
    path_to_log = config.get('settings', 'path_to_log')
    if path_to_log == 'None':
        path = os.path.dirname(os.path.abspath(__file__))
        path_to_log = path[:-7]
    return path_to_log


def check_tracker_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)