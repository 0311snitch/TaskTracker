import sqlite3

from Tracker.lib.models.Column import Column
from Tracker.lib.storage_controller.Project import ProjectStorage


class ColumnStorage:

    @classmethod
    def add_column_to_db(cls,column):
        """
        Добавление колонки в таблицу columns базы данных
        :param column:
        :return:
        """
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("SELECT name FROM columns WHERE project_id==('%s')" % column.project_id)
        data = c.fetchall()
        have = False
        for i in data:
            if i[0] == column.name:
                have = True
        if not have:
            c.execute("INSERT INTO columns (name, desc, project_id) VALUES ('%s', '%s', '%s')" % (column.name,
                                                                                                       column.desc,
                                                                                                       column.project_id))
            conn.commit()
            conn.close()
            return 0
        else:
            print("Колонка с таким названием уже существует в проекте")
            return 1

    @classmethod
    def delete_column_from_db(cls, column):
        """
        Удаление колонки из БД
        :param column:
        :return:
        """
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        c.execute("DELETE FROM columns WHERE name == ('%s') AND project_id==('%s')"%(column.name, column.project_id))
        conn.commit()
        conn.close()
        return 0

    @classmethod
    def get_column(cls, project_name, name):
        """
        Получение колонки с указанным названием
        :param project_name:
        :param name:
        :return:
        """
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        project = ProjectStorage.get_project(project_name)
        c.execute("SELECT * FROM columns WHERE name==('%s') AND project_id==('%s')" % (name,project.id))
        data = c.fetchone()
        column = Column(data[1],data[2],data[3],data[0])
        return column

    @classmethod
    def get_all_columns(cls, project_name):
        """
        Получение всех колонок указанного проекта
        :param project_name:
        :return:
        """
        cols = []
        conn = sqlite3.connect('database.sqlite3')
        c = conn.cursor()
        project = ProjectStorage.get_project(project_name)
        c.execute("SELECT * FROM columns WHERE project_id==('%s')"%project.id)
        data = c.fetchall()
        for i in data:
            column = Column(i[1],i[2],i[3],i[0])
            cols.append(column)
        return cols

