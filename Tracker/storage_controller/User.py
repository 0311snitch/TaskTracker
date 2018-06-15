import sqlite3

import sys

import Tracker.presentations.User as user_view
from Tracker.models.User import *
from Tracker.models.Project import *
from Tracker.Exception import *


class UserStorage:
    @classmethod
    def add_user_to_db(cls, user):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT username FROM users")
        all_usernames = c.fetchall()
        for i in all_usernames:
            if user.username == i[0]:
                raise ProjectWithThisNameAlreadyExist
        print(all_usernames)
        c.execute(
            "INSERT INTO users (username, password, email, token) VALUES ('%s', '%s', '%s', '%s')" % (
            user.username, user.password
            , user.email, user.token))
        conn.commit()
        conn.close()

    @classmethod
    def get_project(cls, name):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT * FROM projects WHERE name==('%s')" % name)
        data = c.fetchone()
        project = Project(data[1], data[2], data[3], None, data[0])
        return project

    @classmethod
    def get_user_by_token(cls, token):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE token==('%s')" % token)
        data = c.fetchone()
        if not data:
            return user_view.failed()
        else:
            user = User(data[1], data[2], data[3], data[4], data[0])
            return user

    @classmethod
    def get_user_by_name(cls, name):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username==('%s')" % name)
        data = c.fetchone()
        if not data:
            return user_view.failed()
        else:
            try:
                user = User(data[1], data[2], data[3], data[4], data[0])
            except:
                raise NoUser
            return user

    @classmethod
    def get_user_by_id(cls, id):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id==('%s')" % id)
        data = c.fetchone()
        if not data:
            return user_view.failed()
        else:
            user = User(data[1], data[2], data[3], data[4], data[0])
            return user

    @classmethod
    def delete_user(cls):
        user = UserStorage.get_current_user()
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username==('%s')" % user.username)
        conn.commit()
        conn.close()

    @classmethod
    def get_password_for_user(cls, username):
        try:
            conn = sqlite3.connect('database.sqlite3')
            c = conn.cursor()
            c.execute("SELECT id, password FROM users WHERE username==('%s') " % username)
            data = c.fetchone()
            conn.close()
            return data[1]
        except:
            return 1

    @classmethod
    def set_password_for_user(cls, user):
        try:
            conn = sqlite3.connect('database.sqlite3')
            c = conn.cursor()
            c.execute("UPDATE users SET password=('%s') WHERE username==('%s')"%(user.password,user.username))
            conn.commit()
            conn.close()
        except:
            print("Ошибка выполнения")

    @classmethod
    def set_username_for_user(cls, user, oldname):
        try:
            conn = sqlite3.connect('database.sqlite3')
            c = conn.cursor()
            c.execute("UPDATE users SET username=('%s') WHERE username==('%s')"%(user.username,oldname))
            conn.commit()
            conn.close()
        except:
            print(error)
            print("Ошибка выполнения")

    @classmethod
    def set_current_user(cls, username):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username==('%s') " % username)
        data = c.fetchone()
        id = data[0]
        c.execute("UPDATE current SET current_id=('%d') WHERE id==('%d')" % (id, 1))
        conn.commit()
        conn.close()

    @staticmethod
    def logout_user_from_storage():
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("UPDATE current SET current_id=('%d') WHERE id==('%d')" % (0, 1))
        conn.commit()
        conn.close()

    @classmethod
    def is_logout(cls):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT current_id FROM current WHERE id==('%d')" % 1)
        id = c.fetchone()[0]
        if id == 0:
            return True
        else:
            return False
