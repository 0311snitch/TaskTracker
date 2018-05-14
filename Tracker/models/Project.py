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

    @classmethod
    def create(self, name, description):
        user = User._get_current_user()
        memberlist = [user, ]
        if user:
            project = Project(name, description, user.user_id, memberlist)
            conn = sqlite3.connect('database.sqlite3')
            c = conn.cursor()
            c.execute("SELECT name FROM projects")
            all_projectnames = c.fetchall()
            for i in all_projectnames:
                if project.name == i[0]:
                    return project_view.failed()
            c.execute("INSERT INTO projects (name, description, user_id) VALUES ('%s', '%s', '%s')" % (project.name,
                                                                                                       project.description,
                                                                                                       project.user_id))
            c.execute("SELECT id FROM projects WHERE name==('%s')" % name)
            id = c.fetchone()
            print(user.user_id, id[0])
            c.execute("INSERT INTO user_project (user_id, project_id) VALUES ('%d', '%d')" % (user.user_id, id[0]))
            conn.commit()
            conn.close()
            return project_view.success_create(project)
        else:
            project_view.need_user()

    @classmethod
    def delete(cls, name):
        project = Project._get_project(name)
        project._delete_with_object()
        return project_view.success_delete()

    @classmethod
    def edit_name(cls, name, new_name):
        project = Project._get_project(name)
        if not project:
            return
        project.name = new_name
        project._save()
        return project_view.success_edit()

    @classmethod
    def edit_description(cls, name):
        project = Project._get_project()

    @classmethod
    def select(cls, name):
        curr_project = Project._get_current_project()
        if curr_project.name == name:
            return project_view.project_already_selected()
        else:
            project = Project._get_project(name)
            project._select_with_object()
            return project_view.project_selected(project)

    @classmethod
    def show_all(cls):
        project_list = []
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT name, description, user_id, id FROM projects")
        data = c.fetchall()
        print(data)
        for i in range(len(data)):
            c.execute("SELECT user_id FROM user_project WHERE project_id==('%d')" % data[i][3])
            project_users = c.fetchall()
            users_to_add = []
            for j in project_users:
                c.execute("SELECT * FROM users WHERE id==('%d')" % j[0])
                user_data = c.fetchone()
                user = User(user_data[1], user_data[2], user_data[3], user_data[0])
                users_to_add.append(user)
            project = Project(data[i][0], data[i][1], data[i][2], users_to_add)
            project_list.append(project)
        return project_view.show_info(project_list)

    @classmethod
    def _get_project(cls, name):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT * FROM projects WHERE name==('%s')" % name)
        project_info = c.fetchone()
        try:
            project = Project(project_info[1], project_info[2], project_info[3], None, project_info[0])
            conn.close()
            return project
        except:
            print("Невозможно получить проект с таким названием")
            conn.close()
            #return -1

    @classmethod
    def _get_current_project(cls):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT current_id FROM current WHERE id==('%d')" % 2)
        project_id = c.fetchone()[0]
        c.execute("SELECT * FROM projects WHERE id==('%d')" % project_id)
        project_data = c.fetchone()
        project = Project(project_data[1], project_data[2], project_data[3], None, project_data[0])
        return project

    def _delete_with_object(self):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("DELETE FROM projects WHERE name=('%s')" % self.name)
        conn.commit()
        conn.close()

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
