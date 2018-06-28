import configparser
import os

DEFAULT_NAME = 'Takinata'
HOME = os.environ['HOME']

DEFAULT = 'Takinata'
DEFAULT_PATH = os.path.join(HOME, DEFAULT)


def create_config(db_path='None', log_path='None', path_to_test_db='None'):
    config = configparser.ConfigParser()
    config.add_section("settings")
    config.set('settings', 'path_to_log', log_path)
    config.set('settings', 'path_to_db', db_path)
    config.set('settings', 'path_to_test_db', path_to_test_db)

    path = os.path.join(HOME, DEFAULT_NAME)
    check_tracker_folder(path)
    path = os.path.join(path, 'config.ini')

    with open(path, 'w') as config_file:
        config.write(config_file)


def load_config():
    config = configparser.ConfigParser()

    path = os.path.join(HOME, DEFAULT_NAME)

    if not os.path.exists(path):
        create_config()
    path = os.path.join(path, 'config.ini')
    config.read(path)
    return config


def get_path_to_db():
    config = load_config()
    path_to_db = config.get('settings', 'path_to_db')
    if path_to_db == 'None':
        path_to_db = os.path.join(HOME, 'Takinata')
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
        path_to_log = os.path.join(HOME, 'Takinata')
    return path_to_log


def check_tracker_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)