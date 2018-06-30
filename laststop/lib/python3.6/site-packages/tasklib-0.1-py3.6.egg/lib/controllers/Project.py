import lib.logger as logger

from lib.Exception import *
from lib.models.Project import Project
from lib.storage_controller.Project import ProjectStorage
from lib.storage_controller.User import UserStorage


class ProjectController:
    @classmethod
    def create(cls, username, password, name, description):
        """
        Create a project with a specified name and description
        :param username:
        :param password:
        :param name:
        :param description:
        :return:
        """
        log_tag = "project_create"
        log = logger.get_logger(log_tag)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            project = Project(name, description, user.user_id)
            ProjectStorage.add_project_to_db(project, user)
            return project
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword


    @classmethod
    def delete(cls, username, password, name):
        """
        Deletes the project with the specified name
        :param username:
        :param password:
        :param name:
        :return:
        """
        log_tag = "project_delete"
        log = logger.get_logger(log_tag)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            project = ProjectStorage.get_project(name)
            ProjectStorage.check_permission(user, project)
            guys = ProjectStorage.get_all_persons_in_project(project)
            for i in guys:
                ProjectController.su_delete_person_from_project(username, password, i, project.name)
            ProjectStorage.delete_with_object(project)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword

    @classmethod
    def add_person_to_project(cls, username, password, project, person):
        """
        Adds an artist to the project
        :param username:
        :param password:
        :param person:
        :param project:
        :return:
        """
        log_tag = "add_person_to_project"
        log = logger.get_logger(log_tag)
        project = ProjectStorage.get_project(project)
        admin = UserStorage.get_user_by_name(username)
        person = UserStorage.get_user_by_name(person)
        if admin.password == password:
            if ProjectStorage.is_admin(admin, project) == 0:
                userlist = ProjectStorage.get_all_persons_in_project(project)
                have = False
                for i in userlist:
                    if i[0] == person.user_id:
                        have = True
                if not have:
                    ProjectStorage.add_person_to_project(person, project)
                else:
                    log.error("User {} is already exist in this project".format(username))
                    raise UserAlreadyExistInProject
            else:
                log.error("You are not the Creator of the project")
                raise UAreNotAdmin
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword

    @classmethod
    def delete_person_from_project(cls, username, password, project, person):
        """
        The removal of the contractor from the project
        :param username:
        :param password:
        :param person:
        :param project:
        :return:
        """
        log_tag = "delete_person_from_project"
        log = logger.get_logger(log_tag)
        project = ProjectStorage.get_project(project)
        admin = UserStorage.get_user_by_name(username)
        person = UserStorage.get_user_by_name(person)
        if admin.password == password:
            if ProjectStorage.is_admin(admin, project) == 0:
                guys = ProjectStorage.get_all_persons_in_project(project)
                have = False
                if guys[0][0] == person.user_id:
                    log.error("User was tried to delete a creator of the project")
                    raise CannotDeleteCreator
                for i in range(len(guys)):
                    if guys[i][0] == person.user_id:
                        have = True
                if not have:
                    log.error("User is not exist")
                    raise UserIsNotExistInProject
                else:
                    ProjectStorage.delete_person_from_project(person, project)
            else:
                log.error("You are not the Creator of the project")
                raise UAreNotAdmin
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword

    @classmethod
    def su_delete_person_from_project(cls, username, password, person, project):
        """
        Delete all the workers from the project, you can also delete the project Creator
        :param username:
        :param password:
        :param person:
        :param project:
        :return:
        """
        log_tag = "su_delete_person_from_project"
        log = logger.get_logger(log_tag)
        project = ProjectStorage.get_project(project)
        admin = UserStorage.get_user_by_name(username)
        person = UserStorage.get_user_by_id(person)
        if admin.password == password:
            ProjectStorage.is_admin(admin, project)
            guys = ProjectStorage.get_all_persons_in_project(project)
            have = False
            for i in range(len(guys)):
                if guys[i][0] == person.user_id:
                    have = True
            if not have:
                log.error("User is not exist")
                raise UserIsNotExistInProject
            else:
                ProjectStorage.delete_person_from_project(person, project)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword

    @classmethod
    def show_all(cls, username, password):
        """
        Displays a list of all projects with the participants of these projects
        :param username:
        :param password:
        :return:
        """
        log_tag = "show_all"
        log = logger.get_logger(log_tag)
        user = UserStorage.get_user_by_name(username)
        new_list = []
        if user.password == password:
            project_list = ProjectStorage.show_all()
            for i in project_list:
                have = False
                guys = ProjectStorage.get_all_persons_in_project(i)
                for j in guys:
                    if user.user_id == j[0]:
                        have = True
                if have:
                    new_list.append(i)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword
        return new_list

    @classmethod
    def edit_name(cls, username, password, project_name, new_name):
        """
        Editing the project name
        :param username:
        :param password:
        :param project_name:
        :param new_name:
        :return:
        """
        log_tag = "edit_name"
        log = logger.get_logger(log_tag)
        person = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        print(project_name)
        if person.password == password:
            ProjectStorage.is_admin(person, project)
            project.name = new_name
            ProjectStorage.save(project)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword

    @classmethod
    def edit_description(cls, username, password, project_name, new_desc):
        """
        Editing the project description
        :param username:
        :param password:
        :param project_name:
        :param new_desc:
        :return:
        """
        log_tag = "edit_description"
        log = logger.get_logger(log_tag)
        person = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        if person.password == password:
            ProjectStorage.is_admin(person, project)
            project.description = new_desc
            ProjectStorage.save(project)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword
