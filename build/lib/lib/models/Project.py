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