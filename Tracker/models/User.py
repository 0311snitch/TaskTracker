import sqlite3
import Tracker.presentations.User as user_view


class User:
    def __init__(self, username, password, email, user_id=None):
        self.username = username
        self.password = password
        self.email = email
        self.user_id = user_id

    def __str__(self):
        return self.username

    @classmethod
    def reg(cls, username, password, email):
        user = User(username, password, email)
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT username FROM users")
        all_usernames = c.fetchall()
        for i in all_usernames:
            if username == i[0]:
                user_view.failed()
                return
        print(all_usernames)
        c.execute(
            "INSERT INTO users (username, password, email) VALUES ('%s', '%s', '%s')" % (user.username, user.password
                                                                                         , user.email))
        conn.commit()
        conn.close()
        return user_view.success_reg(user)

    @classmethod
    def login(cls, username, password):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT current_id FROM current WHERE id==('%d')" % 1)
        id = c.fetchone()[0]
        if id == 0:
            c.execute("SELECT id, password FROM users WHERE username==('%s') " % username)
            data = c.fetchone()
            if password == str(data[1]):
                c.execute("UPDATE current SET current_id=('%d') WHERE id==('%d')" % (data[0], 1))
                conn.commit()
                conn.close()
                return user_view.welcome_back(username)
            else:
                return user_view.failed()
        else:
            return user_view.need_logout()

    @classmethod
    def logout(self):
        user = User._get_current_user()
        if user:
            user._logout_user_with_object()

    def _logout_user_with_object(self):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("UPDATE current SET current_id=('%d') WHERE id==('%d')" % (0, 1))
        conn.commit()
        conn.close()
        return user_view.seeu()

    @classmethod
    def _get_current_user(cls):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT current_id FROM current WHERE id==1")
        id = c.fetchone()[0]
        print(id)
        c.execute("SELECT * FROM users WHERE id==('%d')" % id)
        data = c.fetchone()
        print(data)
        if not data:
            return user_view.logout_error()
        else:
            user = User(data[1], data[2], data[3], data[0])
            return user