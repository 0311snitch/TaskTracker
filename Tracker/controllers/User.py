import hmac, hashlib
from Tracker.storage_controller.User import *


class UserController:
    @classmethod
    def reg(cls, username, password, email):
        sha = hmac.new(bytearray(username,'utf-8'), bytearray(email,'utf-8'), hashlib.sha256).hexdigest()
        shav = sha[:7]
        print(type(shav))
        user = User(username, password, email,shav)
        UserStorage.add_user_to_db(user)
        return user

    @classmethod
    def edit(cls, username, password , param, newparam):
        user = UserStorage.get_user_by_name(username)
        oldname = user.username
        if user.password == password:
            if param == 'name':
                user.username = newparam
            elif param == 'password':
                user.password = newparam
            return user, oldname

    @classmethod
    def delete(cls):
        UserStorage.delete_user()