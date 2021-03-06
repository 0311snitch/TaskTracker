import sqlite3
import lib.conf as conf
from lib.exception import *
from lib.models.task import *
from lib.storage.column import *


class TaskStorage:
    @classmethod
    def add_task_to_db(cls, task):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("INSERT INTO tasks (name, desc, project_id, column_id, user_id, first_date, second_date, "
                  "edit_date, tags, priority, archive, is_subtask) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',"
                  "'%s','%s')" % (task.name, task.desc, task.project_id, task.column_id, task.user_id,
                                  task.first_date, task.second_date, task.edit_date, task.tags, task.priority, 0, task.is_subtask))
        conn.commit()
        conn.close()

    @classmethod
    def delete_task_from_db(cls, task):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id==('%s')"%task.id)
        conn.commit()
        conn.close()

    @classmethod
    def send_to_archive(cls, task):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute(
            "UPDATE tasks SET archive=('%s') WHERE name==('%s') AND column_id==('%s')" % (1, task.name, task.column_id))
        conn.commit()
        conn.close()

    @classmethod
    def save(self, task):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("UPDATE tasks SET name=('%s'),desc=('%s'),project_id=('%s'),column_id=('%s'),user_id=('%s'),"
                  "first_date=('%s'),second_date=('%s'), edit_date=('%s'), tags=('%s'),priority=('%s'),archive=('%s'),"
                  "is_subtask=('%s') WHERE id ==('%s')"
                  % (task.name, task.desc, task.project_id, task.column_id, task.user_id, task.first_date,
                     task.second_date, task.edit_date, task.tags, task.priority, task.archive, task.is_subtask, task.id))
        conn.commit()
        conn.close()

    @classmethod
    def get_task(cls, project_name, column_name, name):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        column = ColumnStorage.get_column(project_name, column_name)
        c.execute("SELECT * FROM tasks WHERE column_id==('%s') AND name==('%s')" % (column.id, name))
        data = c.fetchone()
        try:
            task = Task(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11],
                        data[12], data[0])
        except Exception:
            raise CannotGetProject
        return task

    @classmethod
    def get_all_tasks(cls, project_name, column_name):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        project = ProjectStorage.get_project(project_name)
        column = ColumnStorage.get_column(project_name, column_name)
        c.execute("SELECT * FROM tasks WHERE project_id==('%s') AND column_id==('%s')"%(project.id,column.id))
        data = c.fetchall()
        task_list = []
        conn.close()
        for i in data:
            task = Task(i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[0])
            task_list.append(task)
        return task_list


    @classmethod
    def get_task_by_id(cls, project_name, column_name, id):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        column = ColumnStorage.get_column(project_name, column_name)
        c.execute("SELECT * FROM tasks WHERE column_id==('%s') AND id==('%s')" % (column.id, id))
        data = c.fetchone()
        task = Task(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11],
                    data[12], data[0])
        return task

    @classmethod
    def get_all_subtasks(cls, project_name, column_name, task):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT * FROM task_subtask WHERE task_id == ('%s')"% task.id)
        data = c.fetchall()
        subtask_list = []
        for i in data:
            task = TaskStorage.get_task_by_id(project_name, column_name, i[0])
            subtask_list.append(task)
        return subtask_list

    @classmethod
    def set_subtask(cls, task1, task2):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("INSERT INTO task_subtask (subtask_id, task_id) VALUES ('%s','%s')" % (task1.id, task2.id))
        conn.commit()
        conn.close()

    @classmethod
    def create_table(cls):
        """

        :return:
        """
        path = conf.get_path_to_db()
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("CREATE TABLE 'tasks' (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `name`	TEXT, `desc` TEXT, "
                  "`project_id`	TEXT, `column_id` TEXT, `user_id` TEXT, `first_date` TEXT, `second_date` TEXT, "
                  "`edit_date`	TEXT, `tags` TEXT, `priority` TEXT, `archive` TEXT, `is_subtask` TEXT)")
        c.execute("CREATE TABLE 'task_subtask' (`subtask_id` TEXT, `task_id` TEXT )")
        conn.commit()
        conn.close()
