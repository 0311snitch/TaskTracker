import sqlite3


class Task:
    def __init__(self, name, desc, project_id, column_id, user_id, first_date, second_date, edit_date, tags, priority,
                 archive, is_subtask=0, id=0):
        self.name = name
        self.desc = desc
        self.project_id = project_id
        self.column_id = column_id
        self.user_id = user_id
        self.first_date = first_date
        self.second_date = second_date
        self.edit_date = edit_date
        self.tags = tags
        self.priority = priority
        self.archive = archive
        self.is_subtask = is_subtask
        self.id = id

    def __str__(self):
        return self.name
