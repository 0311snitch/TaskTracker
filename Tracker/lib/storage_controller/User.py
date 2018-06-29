import sqlite3

import Tracker.console.presentations.User as user_view
from Tracker.lib import conf
from Tracker.lib.Exception import *
from Tracker.lib.models.Project import *
from Tracker.lib.models.User import *


class UserStorage:
    @classmethod
    def add_user_to_db(cls, user):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (username, password, email) VALUES ('%s', '%s', '%s')" % (user.username, user.password,
                                                                                         user.email))
        conn.commit()
        conn.close()
        return

    @classmethod
    def get_all_users(cls):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT username FROM users")
        all_usernames = c.fetchall()
        conn.close()
        return all_usernames

    @classmethod
    def get_project(cls, name):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM projects WHERE name==('%s')" % name)
        data = c.fetchone()
        conn.close()
        project = Project(data[1], data[2], data[3], None, data[0])
        return project

    @classmethod
    def get_user_by_name(cls, name):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username==('%s')" % name)
        data = c.fetchone()
        if data is None:
            conn.close()
            raise NoUser
        else:
            user = User(data[1], data[2], data[3], data[0])
            conn.close()
            return user

    @classmethod
    def get_user_by_id(cls, id):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id==('%s')" % id)
        data = c.fetchone()
        if data is None:
            return NoUser
        else:
            user = User(data[1], data[2], data[3], data[0])
            return user

    @classmethod
    def delete_user(cls, name):
        user = UserStorage.get_user_by_name(name)
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username==('%s')" % user.username)
        conn.commit()
        conn.close()

    @classmethod
    def get_password_for_user(cls, username):
        try:
            conn = sqlite3.connect(conf.get_path_to_db())
            c = conn.cursor()
            c.execute("SELECT id, password FROM users WHERE username==('%s') " % username)
            data = c.fetchone()
            return data[1]
        except:
            return 1

    @classmethod
    def set_password_for_user(cls, user):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("UPDATE users SET password=('%s') WHERE username==('%s')" % (user.password, user.username))
        conn.commit()
        conn.close()

    @classmethod
    def set_username_for_user(cls, user, oldname):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("UPDATE users SET username=('%s') WHERE username==('%s')" % (user.username, oldname))
        conn.commit()
        conn.close()

    @classmethod
    def set_current_user(cls, username):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username==('%s') " % username)
        data = c.fetchone()
        id = data[0]
        c.execute("UPDATE current SET current_id=('%d') WHERE id==('%d')" % (id, 1))
        conn.commit()
        conn.close()

    @staticmethod
    def logout_user_from_storage():
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("UPDATE current SET current_id=('%d') WHERE id==('%d')" % (0, 1))
        conn.commit()
        conn.close()

    @classmethod
    def is_logout(cls):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT current_id FROM current WHERE id==('%d')" % 1)
        id = c.fetchone()[0]
        conn.close()
        if id == 0:
            return True
        else:
            return False
