from Tracker.storage_controller.User import *
from Tracker.storage_controller.Column import *
from Tracker.storage_controller.Project import *
from Tracker.models.Column import *


class ColumnController:
    @classmethod
    def create_columm(cls, username, password, project_name, name, description):
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
        print("OLDName - ",column_name)
        print("project-name - ",project_name)
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
        column = ColumnStorage.get_column(project_name, column_name)
        person = UserStorage.get_user_by_name(username)
        if person.password == password:
            project = ProjectStorage.get_project(project_name)
            if ProjectStorage.is_admin(person, project) == 0:
                column.desc = new_desc
                column._save()
