from Tracker.storage_controller.User import *
from Tracker.storage_controller.Task import *
from Tracker.models.Task import *
from Tracker.Exception import *
from datetime import *


class TaskController:
    @classmethod
    def add_task(cls, username, password, project_name, column_name, name, desc, first_date, second_date, tags,
                 priority, is_subtask):
        project = ProjectStorage.get_project(project_name)
        column = ColumnStorage.get_column(project_name, column_name)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            try:
                start = datetime.strptime(first_date, "%d.%m.%Y")
                end = datetime.strptime(first_date, "%d.%m.%Y")
                if end < start:
                    raise EndBeforeStart
            except Exception:
                raise NotDate
            if ProjectStorage.check_permission(user, project) == 0:
                task_names = TaskStorage.get_all_tasks(project_name, column_name)
                have = False
                print(str(date.today()))
                for i in task_names:
                    if i.name == name:
                        have = True
                if not have:
                    task = Task(name, desc, project.id, column.id, user.user_id, first_date, second_date, str(date.today()),tags,
                                priority, 0,
                                is_subtask)
                    TaskStorage.add_task_to_db(task)
                else:
                    raise TaskWithThisNameAlreadyExist(name)
        else:
            raise IncorrentPassword

    @classmethod
    def delete_task(cls, username, password, project_name, column_name, task_name):
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        if user.password == password:
            if ProjectStorage.is_admin(user, project) == 0:
                try:
                    task = TaskStorage.get_task(project_name, column_name, task_name)
                except Exception:
                    raise NoTask
                if task.archive == '1':
                    raise AlreadyInArchive
                else:
                    if task.is_subtask == 1:
                        task.archive = 1
                        task._save()
                    else:
                        list = TaskStorage.get_all_subtasks(project_name, column_name, task)
                        can = True
                        for i in list:
                            if i.archive != '1':
                                can = False
                        if can:
                            task.archive = 1
                            task._save()
                        else:
                            raise CanNotDeleteBecauseSubtasks
            else:
                raise UAreNotAdmin
        else:
            raise IncorrentPassword

    @classmethod
    def show_tasks(cls, username, password, project_name, column_name):
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        column = ColumnStorage.get_column(project_name, column_name)
        if user.password == password:
            if ProjectStorage.check_permission(user, project) == 0:
                tasks = TaskStorage.get_all_tasks(project_name, column_name)
                return tasks
            else:
                raise NoPermission
        else:
            raise IncorrentPassword

    @classmethod
    def set_subtask(cls, username, password, project_name, column_name, task1, task2):
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        if user.password == password:
            if ProjectStorage.check_permission(user, project) == 0:
                task1 = TaskStorage.get_task(project_name, column_name, task1)
                task2 = TaskStorage.get_task(project_name, column_name, task2)
                if task1.is_subtask == '0':
                    if task1.first_date > task2.first_date and task1.second_date < task2.second_date:
                        if task1.priority > task2.priority:
                            raise SubtaskPriorityException
                        else:
                            tasks = TaskStorage.get_all_subtasks(project_name, column_name, task2)
                            can = True
                            for i in tasks:
                                if task1 in tasks:
                                    can = False
                            if can:
                                TaskStorage.set_subtask(task1, task2)
                                task1.is_subtask = 1
                                task1._save()
                            else:
                                raise AlreadySubtask
                    else:
                        raise SubtaskDateException
                else:
                    raise AlreadySubtask
        else:
            raise IncorrentPassword

    @classmethod
    def edit(cls, type_of_edit, username, password, project_name, column_name, task_name, new_value):
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        column = ColumnStorage.get_column(project_name, column_name)
        task = TaskStorage.get_task(project_name, column_name, task_name)
        if user.password == password:
            if ProjectStorage.check_permission(user, project) == 0:
                if type_of_edit == 'name':
                    task.name = new_value
                elif type_of_edit == 'description' or 'desc':
                    task.desc = new_value
                elif type_of_edit == 'tags':
                    task.tags = new_value
                elif type_of_edit == 'priority':
                    try:
                        task.priority = int(new_value)
                    except:
                        TypeErro
                task._save()
        else:
            raise IncorrentPassword