#from Tracker.StorageController.User import *


class User:
    def __init__(self, username, password, email, user_id=None):
        self.username = username
        self.password = password
        self.email = email
        self.user_id = user_id

    def __str__(self):
        return self.username
