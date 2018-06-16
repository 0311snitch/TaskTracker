import Tracker.console.presentations.User as user_view
from Tracker.lib.models.Column import Column
from Tracker.lib.storage_controller.Column import ColumnStorage
from Tracker.lib.storage_controller.Project import *
from Tracker.lib.storage_controller.User import *


class ColumnController:
    @classmethod
    def create_columm(cls, username, password, project_name, name, description):
        """
        Создает сущнность типа "Колонка" для указанного проекта
        :param username:
        :param password:
        :param project_name:
        :param name:
        :param description:
        :return:
        """
        try:
            user = UserStorage.get_user_by_name(username)
            if user.password == password:
                project = ProjectStorage.get_project(project_name)
                if ProjectStorage.is_admin(user, project) == 0:
                    column = Column(name, description, project.id)
                    ColumnStorage.add_column_to_db(column)
            else:
                print(user_view.invalid_password())
        except:
            print(user_view.failed())

    @classmethod
    def delete_column(cls, username, password, project_name, name):
        """
        Удаляет колонку с указанным названием из указанного проекта
        :param username:
        :param password:
        :param project_name:
        :param name:
        :return:
        """
        try:
            user = UserStorage.get_user_by_name(username)
            if user.password == password:
                column = ColumnStorage.get_column(project_name, name)
                project = ProjectStorage.get_project(project_name)
                if ProjectStorage.is_admin(user, project):
                    ColumnStorage.delete_column_from_db(column)
                else:
                    print(user_view.u_are_not_admin())
            else:
                print(user_view.invalid_password())
        except:
            print(user_view.failed())

    @classmethod
    def show_all(cls, username, password, project_name):
        """
        Осуществляет показ всех колонок проекта
        :param username:
        :param password:
        :param project_name:
        :return:
        """
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        if user.password == password:
            if ProjectStorage.check_permission(user, project) == 0:
                cols = ColumnStorage.get_all_columns(project_name)
                return cols
        else:
            print(user_view.invalid_password())

    @classmethod
    def edit_name(cls, username, password, project_name, column_name, new_name):
        """
        Изменение названия проекта
        :param username:
        :param password:
        :param project_name:
        :param column_name:
        :param new_name:
        :return:
        """
        column = ColumnStorage.get_column(project_name, column_name)
        person = UserStorage.get_user_by_name(username)
        if person.password == password:
            project = ProjectStorage.get_project(project_name)
            if ProjectStorage.is_admin(person, project) == 0:
                column.name = new_name
                column._save()
                return 0

    @classmethod
    def edit_desc(cls, username, password, project_name, column_name, new_desc):
        """
        Изменение описания проекта
        :param username:
        :param password:
        :param project_name:
        :param column_name:
        :param new_desc:
        :return:
        """
        column = ColumnStorage.get_column(project_name, column_name)
        person = UserStorage.get_user_by_name(username)
        if person.password == password:
            project = ProjectStorage.get_project(project_name)
            if ProjectStorage.is_admin(person, project) == 0:
                column.desc = new_desc
                column._save()
