

class RegularTask:
    def __init__(self, name, desc, project_id, column_id, user_id, first_date, second_date, step, edit_date, tags, priority,
                 archive, id=0):
        self.name = name
        self.desc = desc
        self.project_id = project_id
        self.column_id = column_id
        self.user_id = user_id
        self.first_date = first_date
        self.second_date = second_date
        self.step = step
        self.edit_date = edit_date
        self.tags = tags
        self.priority = priority
        self.archive = archive
        self.id = id