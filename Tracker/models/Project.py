import sqlite3
from Tracker.models.User import *
import Tracker.presentations.Project as project_view


class Project:
    def __init__(self, name, description, user_id, members=None, id=None):
        if members is None:
            members = []
        self.name = name
        self.description = description
        self.user_id = user_id
        self.members = members
        self.id = id

    def __str__(self):
        return self.name

    def _save(self):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute(
            "UPDATE projects SET name=('%s'),description=('%s') WHERE id==('%d')" % (self.name, self.description,
                                                                                     self.id))
        conn.commit()
        conn.close()

    def _select_with_object(self):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("UPDATE current SET current_id=('%d') WHERE id==('%d')" % (self.id, 2))
        conn.commit()
