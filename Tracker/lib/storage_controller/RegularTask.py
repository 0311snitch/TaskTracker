import sqlite3

from Tracker.lib.models.RegularTask import *
from Tracker.lib.storage_controller.Column import *
from Tracker.lib.storage_controller.Project import *


class RegularTaskStorage:
    @classmethod
    def add_task_to_db(cls, task):
        """
        Добавление регулярной задачи в БД
        :param task:
        :return:
        """
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute(
            "INSERT INTO regular_task (name, desc, project_id, column_id, user_id, first_date, second_date, step, "
            "edit_date, tags, priority, archive) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',"
            "'%s','%s')" % (task.name, task.desc, task.project_id, task.column_id, task.user_id,
                            task.first_date, task.second_date, task.step, task.edit_date, task.tags, task.priority,
                            0))
        conn.commit()
        conn.close()

    @classmethod
    def get_all_tasks(cls, project_name, column_name):
        """
        Получение списка всех регулярных задач для указанной колонки
        :param project_name:
        :param column_name:
        :return:
        """
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        print("CHECK THIS ", column_name)
        project = ProjectStorage.get_project(project_name)
        column = ColumnStorage.get_column(project_name, column_name)
        c.execute("SELECT * FROM regular_task WHERE project_id==('%s') AND column_id==('%s')" % (project.id, column.id))
        data = c.fetchall()
        task_list = []
        for i in data:
            task = RegularTask(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[0])
            task_list.append(task)
        conn.close()
        return task_list
