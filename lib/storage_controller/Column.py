import sqlite3

import lib.conf as conf
from lib.models.Column import Column
from lib.storage_controller.Project import ProjectStorage
from lib.Exception import *


class ColumnStorage:

    @classmethod
    def add_column_to_db(cls, column):
        """
        Добавление колонки в таблицу columns базы данных
        :param column:
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("SELECT name FROM columns WHERE project_id==('%s')" % column.project_id)
        data = c.fetchall()
        have = False
        for i in data:
            if i[0] == column.name:
                have = True
        if not have:
            c.execute("INSERT INTO columns (name, desc, project_id) VALUES ('%s', '%s', '%d')" % (column.name,
                                                                                                  column.desc,
                                                                                                  column.project_id))
            conn.commit()
            conn.close()
        else:
            raise ColumnWithThisNameAlreadyExist


    @classmethod
    def save(self, column):
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute(
            "UPDATE columns SET name=('%s'),desc=('%s'),project_id=('%s') WHERE id==('%d')" % (column.name, column.desc,
                                                                                     column.project_id, column.id))
        conn.commit()
        conn.close()

    @classmethod
    def delete_column_from_db(cls, column):
        """
        Удаление колонки из БД
        :param column:
        :return:
        """
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        c.execute("DELETE FROM columns WHERE name == ('%s') AND project_id==('%s')" % (column.name, column.project_id))
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
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        project = ProjectStorage.get_project(project_name)
        c.execute("SELECT * FROM columns WHERE name==('%s') AND project_id==('%s')" % (name, project.id))
        data = c.fetchone()
        try:
            column = Column(data[1], data[2], data[3], data[0])
            conn.close()
            return column
        except:
            conn.close()
            raise NoColumnWithThisName

    @classmethod
    def get_all_columns(cls, project_name):
        """
        Получение всех колонок указанного проекта
        :param project_name:
        :return:
        """
        cols = []
        conn = sqlite3.connect(conf.get_path_to_db())
        c = conn.cursor()
        project = ProjectStorage.get_project(project_name)
        c.execute("SELECT * FROM columns WHERE project_id==('%s')" % project.id)
        data = c.fetchall()
        for i in data:
            column = Column(i[1], i[2], i[3], i[0])
            cols.append(column)
        return cols
