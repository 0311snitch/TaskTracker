import sqlite3
import lib.conf as conf

from lib.Exception import *
from lib.models.Project import *
from lib.models.User import *


class ProjectStorage:
    @classmethod
    def add_project_to_db(cls, project, user):
        """
        Добавление проекта в БД
        :param project:
        :param user:
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
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
            c.execute("INSERT INTO user_project (user_id, project_id) VALUES ('%d', '%d')" % (user.user_id, id[0]))
            conn.commit()
            conn.close()
        else:
            raise ProjectWithThisNameAlreadyExist()

    @classmethod
    def get_all_persons_in_project(cls, project):
        """
        Получение всех исполнителей указанного проекта
        :param project:
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT user_id FROM user_project WHERE project_id ==('%s')" % project.id)
        data = c.fetchall()
        return data

    @classmethod
    def get_all_projects(cls, user_id):
        """
        Получение всех проектов для пользователя
        :param user_id:
        :return:
        """
        projects = []
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM projects WHERE user_id ==('%s')" % user_id)
        data = c.fetchall()
        for i in data:
            project = Project(i[1],i[2],i[3],None,i[0])
            projects.append(project)
        return projects

    @classmethod
    def add_person_to_project(cls, person, project):
        """
        Добавляет указанного пользователя в проект
        :param person:
        :param project:
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("INSERT INTO user_project (user_id, project_id) VALUES ('%d','%d')"%(person.user_id,project.id))
        conn.commit()
        conn.close()

    @classmethod
    def delete_person_from_project(cls, person, project):
        """
        Удаление пользователя из проекта
        :param person:
        :param project:
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("DELETE FROM user_project WHERE user_id ==('%s') AND project_id==('%s')"% (person.user_id, project.id))
        conn.commit()
        conn.close()

    @classmethod
    def delete_with_object(cls, project):
        """
        Удаление проекта с указанным названием
        :param project:
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("DELETE FROM projects WHERE name=('%s')" % project.name)
        conn.commit()
        conn.close()

    @classmethod
    def get_project(cls, name):
        """
        Получение проекта с указанным названием
        :param name:
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM projects WHERE name==('%s')" % name)
        project_info = c.fetchone()
        try:
            project = Project(project_info[1], project_info[2], project_info[3], None, project_info[0])
            conn.close()
            return project
        except:
            conn.close()
            raise CannotGetProject

    @classmethod
    def show_all(cls):
        """
        Вывод списка всех проектов с их исполнителями
        :return:
        """
        project_list = []
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT name, description, user_id, id FROM projects")
        data = c.fetchall()
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
        """
        Проверяет наличие доступа к указанному проекту для данного пользователя
        :param person:
        :param project:
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        guys = ProjectStorage.get_all_persons_in_project(project)
        for i in guys:
            if i[0] == person.user_id:
                return
        raise NoPermission

    @classmethod
    def is_admin(cls, person, project):
        """
        Проверяет является ли указанный пользователь создателем проекта
        :param person:
        :param project:
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        guys = ProjectStorage.get_all_persons_in_project(project)
        if guys[0][0] == person.user_id:
            pass
        else:
            raise UAreNotAdmin

    @classmethod
    def save(self, project):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute(
            "UPDATE projects SET name=('%s'),description=('%s') WHERE id==('%d')" % (project.name, project.description,
                                                                                     project.id))
        conn.commit()
        conn.close()
