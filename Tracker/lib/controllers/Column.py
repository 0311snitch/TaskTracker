import Tracker.console.presentations.User as user_view
import Tracker.lib.logger as logger
from Tracker.lib.models.Column import Column
from Tracker.lib.storage_controller.Column import ColumnStorage
from Tracker.lib.storage_controller.Project import *
from Tracker.lib.storage_controller.User import *


class ColumnController:
    @classmethod
    def create_columm(cls, username, password, project_name, name, description):
        """
        Creates a column for the specified project
        :param username:
        :param password:
        :param project_name:
        :param name:
        :param description:
        :return:
        """
        log_tag = "create_column"
        log = logger.get_logger(log_tag)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            project = ProjectStorage.get_project(project_name)
            ProjectStorage.is_admin(user, project)
            column = Column(name, description, project.id)
            ColumnStorage.add_column_to_db(column)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword

    @classmethod
    def delete_column(cls, username, password, project_name, name):
        """
        Removes a column with the specified name from the specified project
        :param username:
        :param password:
        :param project_name:
        :param name:
        :return:
        """
        log_tag = "delete_column"
        log = logger.get_logger(log_tag)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            column = ColumnStorage.get_column(project_name, name)
            project = ProjectStorage.get_project(project_name)
            ProjectStorage.is_admin(user, project)
            ColumnStorage.delete_column_from_db(column)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword

    @classmethod
    def show_all(cls, username, password, project_name):
        """
        Displays all columns of the project
        :param username:
        :param password:
        :param project_name:
        :return:
        """
        log_tag = "show_all_columns"
        log = logger.get_logger(log_tag)
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        if user.password == password:
            ProjectStorage.check_permission(user, project)
            cols = ColumnStorage.get_all_columns(project_name)
            return cols
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword

    @classmethod
    def edit_name(cls, username, password, project_name, column_name, new_name):
        """
        The change of name of the project
        :param username:
        :param password:
        :param project_name:
        :param column_name:
        :param new_name:
        :return:
        """
        log_tag = "edit_column_name"
        log = logger.get_logger(log_tag)
        column = ColumnStorage.get_column(project_name, column_name)
        person = UserStorage.get_user_by_name(username)
        if person.password == password:
            project = ProjectStorage.get_project(project_name)
            ProjectStorage.is_admin(person, project)
            column.name = new_name
            ColumnStorage.save(column)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword

    @classmethod
    def edit_desc(cls, username, password, project_name, column_name, new_desc):
        """
        Change the description of the project
        :param username:
        :param password:
        :param project_name:
        :param column_name:
        :param new_desc:
        :return:
        """
        log_tag = "edit_column_description"
        log = logger.get_logger(log_tag)
        column = ColumnStorage.get_column(project_name, column_name)
        person = UserStorage.get_user_by_name(username)
        if person.password == password:
            project = ProjectStorage.get_project(project_name)
            ProjectStorage.is_admin(person, project)
            column.desc = new_desc
            ColumnStorage.save(column)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword
