import sqlite3
from Tracker.models.Project import *
from Tracker.Exception import *


class ProjectStorage:
    @classmethod
    def add_project_to_db(cls, project, user):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT name, user_id FROM projects")
        all_projectnames = c.fetchall()
        yep = False
        for i in all_projectnames:
            if project.name == i[0] and user.user_id == i[1]:
                yep = True
        if not yep:
            c.execute("INSERT INTO projects (name, description, user_id) VALUES ('%s', '%s', '%s')" % (project.name,
                                                                                                       project.description,
                                                                                                       user.user_id))
            conn.commit()
            c.execute("SELECT id FROM projects WHERE name==('%s')" % project.name)
            id = c.fetchone()
            print("4len")
            print(user.user_id)
            c.execute("INSERT INTO user_project (user_id, project_id) VALUES ('%d', '%d')" % (user.user_id, id[0]))
            conn.commit()
            conn.close()
        else:
            raise ProjectWithThisNameAlreadyExist()

    @classmethod
    def get_all_persons_in_project(cls, project):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT user_id FROM user_project WHERE project_id ==('%s')" % project.id)
        data = c.fetchall()
        print(data)
        return data

    @classmethod
    def add_person_to_project(cls, person, project):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("INSERT INTO user_project (user_id, project_id) VALUES ('%d','%d')"%(person.user_id,project.id))
        conn.commit()
        conn.close()

    @classmethod
    def delete_person_from_project(cls, person, project):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("DELETE FROM user_project WHERE user_id ==('%d')"% person.user_id)
        conn.commit()
        conn.close()

    @classmethod
    def delete_with_object(cls, project):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("DELETE FROM projects WHERE name=('%s')" % project.name)
        conn.commit()
        conn.close()

    @classmethod
    def get_project(cls, name):
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
            # return -1

    @classmethod
    def show_all(cls):
        project_list = []
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT name, description, user_id, id FROM projects")
        data = c.fetchall()
        #print(data)
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
        return project_list

    @classmethod
    def check_permission(cls, person, project):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        print("WOW",project)
        guys = ProjectStorage.get_all_persons_in_project(project)
        print(guys)
        for i in guys:
            if i[0] == person.user_id:
                return 0
        return 1

    @classmethod
    def is_admin(cls, person, project):
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        guys = ProjectStorage.get_all_persons_in_project(project)
        if guys[0][0] == person.user_id:
            return 0
        return 1
