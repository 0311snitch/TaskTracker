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

    def _save(self):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("UPDATE tasks SET name=('%s'),desc=('%s'),project_id=('%s'),column_id=('%s'),user_id=('%s'),"
                  "first_date=('%s'),second_date=('%s'), edit_date=('%s'), tags=('%s'),priority=('%s'),archive=('%s'),"
                  "is_subtask=('%s') WHERE id ==('%s')"
                  % (self.name, self.desc, self.project_id, self.column_id, self.user_id, self.first_date,
                     self.second_date, self.edit_date, self.tags, self.priority, self.archive, self.is_subtask, self.id))
        conn.commit()
        conn.close()
