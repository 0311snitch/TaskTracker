import lib.logger as logger

from datetime import *
from lib.storage_controller.RegularTask import *
from lib.storage_controller.User import *


class RegularTaskController:
    @classmethod
    def add_task(cls, username, password, project_name, column_name, name, desc, first_date, second_date, step,
                 type_of_step, tags, priority):
        """
        Создает регулярную задачу в выбранной колонке выбранного проекта с указанным шагом перехода и указанными времен-
        ными границами
        :param username:
        :param password:
        :param project_name:
        :param column_name:
        :param name:
        :param desc:
        :param first_date:
        :param second_date:
        :param step:
        :param edit_date:
        :param tags:
        :param priority:
        :return:
        """
        log_tag = "add_regular_task"
        log = logger.get_logger(log_tag)
        project = ProjectStorage.get_project(project_name)
        column = ColumnStorage.get_column(project_name, column_name)
        user = UserStorage.get_user_by_name(username)
        if user.password == password:
            try:
                start = datetime.strptime(first_date, "%d.%m.%Y")
                end = datetime.strptime(first_date, "%d.%m.%Y")
                if end < start:
                    log.error("EndDate is before StartDate")
                    raise EndBeforeStart
            except Exception:
                log.error("It's not a date")
                raise NotDate
            ProjectStorage.check_permission(user, project)
            task_names = RegularTaskStorage.get_all_tasks(project_name, column_name)
            have = False
            for i in task_names:
                if i.name == name:
                    have = True
            if not have:
                regular_task = RegularTask(name, desc, project.id, column.id, user.user_id, first_date, second_date,
                                           step, type_of_step, str(date.today()), tags, priority, 0)
                RegularTaskStorage.add_task_to_db(regular_task)
                return regular_task
            else:
                log.error("Task with this name is already exist")
                raise TaskWithThisNameAlreadyExist(name)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword

    @classmethod
    def delete_task(cls, username, password, project_name, column_name, task_name):
        """
        Delete the specified task
        :param username:
        :param password:
        :param project_name:
        :param column_name:
        :param task_name:
        :return:
        """
        log_tag = "task_delete"
        log = logger.get_logger(log_tag)
        user = UserStorage.get_user_by_name(username)
        project = ProjectStorage.get_project(project_name)
        if user.password == password:
            ProjectStorage.is_admin(user, project)
            try:
                task = RegularTaskStorage.get_task(project_name, column_name, task_name)
            except Exception:
                log.error("There is no task with this name")
                raise NoTask
            RegularTaskStorage.delete_task_from_db(task)
        else:
            log.error("Incorrect password for {}".format(username))
            raise IncorrentPassword
