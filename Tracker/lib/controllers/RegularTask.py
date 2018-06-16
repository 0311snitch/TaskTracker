from datetime import *

from Tracker.lib.storage_controller.RegularTask import *
from Tracker.lib.storage_controller.User import *


class RegularTaskController:
    @classmethod
    def add_task(cls, username, password, project_name, column_name, name, desc, first_date, second_date, step, edit_date, tags,
                 priority):
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
                task_names = RegularTaskStorage.get_all_tasks(project_name, column_name)
                have = False
                print(str(date.today()))
                for i in task_names:
                    if i.name == name:
                        have = True
                if not have:
                    regular_task = RegularTask(name, desc, project.id, column.id, user.user_id, first_date, second_date, step, edit_date, str(date.today()),tags,
                                priority, 0)
                    RegularTaskStorage.add_task_to_db(regular_task)
                    return regular_task
                else:
                    raise TaskWithThisNameAlreadyExist(name)
            else:
                raise NoPermission
        else:
            raise IncorrentPassword
