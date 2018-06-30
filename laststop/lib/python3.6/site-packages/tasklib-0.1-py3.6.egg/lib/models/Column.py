import sqlite3


class Column:
    def __init__(self, name, desc, project_id, id = None):
        self.name = name
        self.desc = desc
        self.project_id  = project_id
        self.id = id

    def __str__(self):
        return self.name