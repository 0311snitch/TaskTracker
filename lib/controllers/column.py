import lib.logger as logger
from lib.exception import *
from lib.models.column import Column
from lib.storage.column import ColumnStorage
from lib.storage.project import *
from lib.storage.user import *


class ColumnController:
    log_tag = "ColumnController"

    @classmethod
    def create_columm(cls, username, password, project_name, name, description):
        """
        Creates a column for the specified project
        :param username: who want to create a new column
        :param password: user password
        :param project_name: name of the project where user want to create a column
        :param name: name of the column
        :param description: description of the column
        :return:
        """
        log = logger.get_logger(ColumnController.log_tag)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            project = ProjectStorage.get_project(project_name)
            ProjectStorage.is_admin(user, project)
            column = Column(name, description, project.id)
            log.info("")
            ColumnStorage.add_column_to_db(column)
        else:
            log.error("Incorrect password for %s", username)
            raise WrongPassword

    @classmethod
    def delete_column(cls, username, password, project_name, name):
        """
        Removes a column with the specified name from the specified project
        :param username: name of user, whitch want to delete a column
        :param password: user password
        :param project_name: name of project where column is
        :param name: name of column to delete
        :return:
        """
        log = logger.get_logger(ColumnController.log_tag)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            column = ColumnStorage.get_column(project_name, name)
            project = ProjectStorage.get_project(project_name)
            ProjectStorage.is_admin(user, project)
            ColumnStorage.delete_column_from_db(column)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def show_all(cls, username, password, project_name):
        """
        Displays all columns of the project
        :param username: user, which want to watch column list in project
        :param password: user password
        :param project_name: the project whose columns you want to show
        :return:
        """
        log = logger.get_logger(ColumnController.log_tag)
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        if user.password == password:
            ProjectStorage.check_permission(user, project)
            cols = ColumnStorage.get_all_columns(project_name)
            return cols
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def edit_name(cls, username, password, project_name, column_name, new_name):
        """
        The change of name of the project
        :param username: username of column creator
        :param password: password of creator
        :param project_name: project name of project where column is
        :param column_name: column name
        :param new_name: new name of column
        :return:
        """
        log = logger.get_logger(ColumnController.log_tag)
        column = ColumnStorage.get_column(project_name, column_name)
        person = UserStorage.get_user_by_name(username)
        if person.password == password:
            project = ProjectStorage.get_project(project_name)
            ProjectStorage.is_admin(person, project)
            column.name = new_name
            ColumnStorage.save(column)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def edit_desc(cls, username, password, project_name, column_name, new_desc):
        """
        Change the description of the project
        :param username: username of column creator
        :param password: password of creator
        :param project_name: project name of project where column is
        :param column_name: column name
        :param new_desc: new description of column
        :return:
        """
        log = logger.get_logger(ColumnController.log_tag)
        column = ColumnStorage.get_column(project_name, column_name)
        person = UserStorage.get_user_by_name(username)
        if person.password == password:
            project = ProjectStorage.get_project(project_name)
            ProjectStorage.is_admin(person, project)
            column.desc = new_desc
            ColumnStorage.save(column)
        else:
            log.error("Incorrect password for {}".format(username))
            raise WrongPassword

    @classmethod
    def create_table(cls):
        ColumnStorage.create_table()