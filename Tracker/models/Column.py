import sqlite3


class Column:
    def __init__(self, name, desc, project_id, id = None):
        self.name = name
        self.desc = desc
        self.project_id  = project_id
        self.id = id

    def _save(self):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute(
            "UPDATE columns SET name=('%s'),desc=('%s'),project_id=('%s') WHERE id==('%d')" % (self.name, self.desc,
                                                                                     self.project_id, self.id))
        conn.commit()
        conn.close()

    def _select_with_object(self):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("UPDATE current SET current_id=('%d') WHERE id==('%d')" % (self.id, 3))
        conn.commit()