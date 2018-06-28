import Tracker.lib.logger as logger

from Tracker.lib.models.User import User
from Tracker.lib.storage_controller.User import UserStorage
from Tracker.lib.Exception import *


class UserController:
    @classmethod
    def reg(cls, username, password, email):
        """
        User registration with the specified data
        :param username:
        :param password:
        :param email:
        :return:
        """
        log_tag = "UserReg"
        log = logger.get_logger(log_tag)
        user = User(username, password, email)
        users = UserStorage.get_all_users()
        have = False
        for i in users:
            if i[0] == user.username:
                have = True
        if not have:
            UserStorage.add_user_to_db(user)
            return user
        else:
            log.error("User with this name is already exist")
            raise UserAlreadyExist

    @classmethod
    def edit(cls, username, password, param, newparam):
        """
        Editing user information
        :param username:
        :param password:
        :param param:
        :param newparam:
        :return:
        """
        log_tag = "UserEdit"
        log = logger.get_logger(log_tag)
        user = UserStorage.get_user_by_name(username)
        oldname = user.username
        if user.password == password:
            if param == 'name':
                user.username = newparam
                UserStorage.set_username_for_user(user, oldname)
            elif param == 'password':
                user.password = newparam
                UserStorage.set_password_for_user(user)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword

    @classmethod
    def delete(cls, username, password):
        """
        Remove a user with the specified name
        :param name:
        :return:
        """
        log_tag = "UserDelete"
        log = logger.get_logger(log_tag)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            UserStorage.delete_user(username)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword
