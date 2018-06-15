from Tracker.storage_controller.Project import *
from Tracker.storage_controller.User import *
from Tracker.models.Project import *


class ProjectController:
    @classmethod
    def create(cls, username, password, name, description):
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            project = Project(name, description, user.user_id)
            ProjectStorage.add_project_to_db(project, user)
            return project
        else:
            raise IncorrentPassword

    @classmethod
    def delete(cls, username, password, name):
        try:
            user = UserStorage.get_user_by_name(username)
            if user.password == password:
                project = ProjectStorage.get_project(name)
                if ProjectStorage.check_permission(user, project) == 0:
                    guys = ProjectStorage.get_all_persons_in_project(project)
                    for i in guys:
                        ProjectController.su_delete_person_from_project(username, password, i, project.name)
                    ProjectStorage.delete_with_object(project)
                else:
                    project_view.permission_error()
                    sys.exit()
            else:
                user_view.invalid_password()
                sys.exit()
        except:
            project_view.delete_error()
            sys.exit()

    @classmethod
    def add_person_to_project(cls, username, password, person, project):
        try:
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
                        print(project_view.already_exist())
                        return 0
                else:
                    print(user_view.u_are_not_admin())
                    return 0
            else:
                print(user_view.invalid_password())
                return 0
        except:
            print(user_view.failed())
            return 0

    @classmethod
    def delete_person_from_project(cls, username, password, person, project):
        try:
            project = ProjectStorage.get_project(project)
            admin = UserStorage.get_user_by_name(username)
            person = UserStorage.get_user_by_name(person)
            if admin.password == password:
                if ProjectStorage.is_admin(admin, project) == 0:
                    guys = ProjectStorage.get_all_persons_in_project(project)
                    have = False
                    if guys[0][0] == person.user_id:
                        print(project_view.cannot_delete_admin())
                        return 0
                    for i in range(len(guys)):
                        if guys[i][0] == person.user_id:
                            have = True
                    if not have:
                        print(project_view.not_exist())
                    else:
                        try:
                            ProjectStorage.delete_person_from_project(person, project)
                        except:
                            print(project_view.not_exist())
                else:
                    print(user_view.u_are_not_admin())
        except:
            print(user_view.failed())

    @classmethod
    def su_delete_person_from_project(cls, username, password, person, project):
        try:
            project = ProjectStorage.get_project(project)
            admin = UserStorage.get_user_by_name(username)
            person = UserStorage.get_user_by_id(person)
            if admin.password == password:
                if ProjectStorage.is_admin(admin, project) == 0:
                    guys = ProjectStorage.get_all_persons_in_project(project)
                    have = False
                    for i in range(len(guys)):
                        if guys[i][0] == person.user_id:
                            have = True
                    if not have:
                        print(project_view.not_exist())
                    else:
                        try:
                            ProjectStorage.delete_person_from_project(person, project)
                        except:
                            print(project_view.not_exist())
                else:
                    print(user_view.u_are_not_admin())
        except:
            print(user_view.failed())

    @classmethod
    def show_all(cls, username, password):
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
        return new_list

    @classmethod
    def edit_name(cls, username, password, project_name, new_name):
        try:
            person = UserStorage.get_user_by_name(username)
            project = ProjectStorage.get_project(project_name)
            print(project_name)
            if person.password == password:
                if ProjectStorage.is_admin(person, project) == 0:
                    project.name = new_name
                    project._save()
                    return project_view.success_edit()
                else:
                    print(user_view.u_are_not_admin())
            else:
                print(user_view.invalid_password())
        except:
            print(user_view.failed())

    @classmethod
    def edit_description(cls, username, password, project_name, new_desc):
        try:
            person = UserStorage.get_user_by_name(username)
            project = ProjectStorage.get_project(project_name)
            if person.password == password:
                if ProjectStorage.is_admin(person, project) == 0:
                    project.description = new_desc
                    project._save()
                    return project_view.success_edit()
                else:
                    print(user_view.u_are_not_admin())
            else:
                print(user_view.invalid_password())
        except:
            print(user_view.failed())
