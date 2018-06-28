import os
import Tracker.console.config as conf


def get_path_to_logger():
    try:
        path = conf.get_path_to_log()
        return path
    except:
        path = os.path.dirname(os.path.abspath(__file__))
        return path[:-3]


def get_path_to_db():
    try:
        path = conf.get_path_to_db()
        return path
    except:
        path = os.path.dirname(os.path.abspath(__file__))
        path = path[:-3]
        path = os.path.join(path, 'database.sqlite3')
        print(path)
        return path
