import logging

from datetime import datetime
from enum import Enum
from Tracker.console.presentations.Project import *
from Tracker.console.presentations.RegularTask import *
from Tracker.console.presentations.Task import *
import Tracker.console.presentations.Column as column_view
from Tracker.lib.controllers.Column import *
from Tracker.lib.controllers.Project import *
from Tracker.lib.controllers.RegularTask import *
from Tracker.lib.controllers.Task import *
from Tracker.lib.controllers.User import *
from Tracker.lib.storage_controller.Task import *
from Tracker.lib.storage_controller.User import *
from Tracker.lib.logger import *


class Categories(Enum):
    user = 0
    project = 1
    column = 2
    task = 3
    regular_task = 4
    subtask = 5


class SubCategories(Enum):
    add = 0
    delete = 1
    edit = 2
    show = 3
    register = 4
    login = 5
    logout = 6
    select = 7
    members = 8
    archive = 9
    subtask = 10


def set_category(arg):
    return Categories[arg]


def set_subcategory(arg):
    return SubCategories[arg]


def incorrent_args_len():
    print('Некорректное количество аргументов. Для получения информации о командах введите help')


def not_subcategory():
    print("Ошибка исполнения. Необходимо ввести подкоманду")


def check_notifications(username, password):
    """
    Проверяет задачи на то как скоро дедалйн и если существуют задачи, в которых дедлайн раньше, чем через 20 дней, то
    выводится уведомление
    :param username:
    :param password:
    :return:
    """
    user = UserStorage.get_user_by_name(username)
    if user.password == password:
        projects = ProjectStorage.get_all_projects(user.user_id)
        task_list = []
        for i in projects:
            cols = ColumnStorage.get_all_columns(i.name)
            for j in cols:
                tasks = TaskStorage.get_all_tasks(i.name, j.name)
                task_list.append(tasks)
        a = datetime.today().strftime("%d.%m.%Y")
        for x in task_list:
            for y in x:
                date = y.second_date.split(".")
                new_date = datetime(int(date[2]), int(date[1]), int(date[0]))
                today_date = datetime.today()
                if new_date.year == today_date.year and new_date.month == today_date.month:
                    if 10 <= new_date.day - today_date.day < 20:
                        print("Необходимо заняться задачей {}. До времени окончания задачи осталось всего лишь {} "
                              "дня(ей).".format(y.name, new_date.day - today_date.day))
                    elif 1 <= new_date.day - today_date.day < 5:
                        print("ВАМ СРОЧНО НЕОБХОДИМО ЗАНЯТЬСЯ ЗАДАЧЕЙ '{}' . ОСТАЛОСЬ {} дня(ей).".format(
                            y.name, new_date.day - today_date.day))
                    elif new_date.day - today_date.day < 1:
                        print("Вы просрочили задачу {}. Хорошим решением было бы отправить её в архив".format(y.name))
    else:
        raise IncorrentPassword


def parse(args):
    """
    Функция, которая получает список всех параметров, выделяет категорию и подкатегорию и передает управление в следую-
    щий обработчик
    :param args:
    :return:
    """
    count = len(args)
    if count == 0:
        incorrent_args_len()
        LOGGER.error("Введено некорректное количество аргументов\r\n\r\n")
    else:
        try:
            category = set_category(args[0])
            subcategory = set_subcategory(args[1])
            LOGGER.info("Список полученных аргментов : {}".format(args))
            if category == Categories.user:
                parse_user(subcategory, args[2:])
            check_notifications(args[2], args[3])
            if category == Categories.project:
                parse_project(subcategory, args[2:])
            elif category == Categories.column:
                parse_column(subcategory, args[2:])
            elif category == Categories.task:
                parse_task(subcategory, args[2:])
            elif category == Categories.regular_task:
                parse_regular_task(subcategory, args[2:])
        except BaseException as error:
            LOGGER.error(error)
            print(error)


def parse_user(subcategory, args):
    """
    Обработчик для категории "Пользователь"
    :param subcategory:
    :param args:
    :return:
    """
    if subcategory == SubCategories.register:
        if len(args) != 3:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".
                    format(3, len(args)))
            user_view.reg_format()
        else:
            LOGGER.info("Попытка зарегестрировать пользователя с именем {}, паролем {} и e-mail {}"
                        .format(args[0], args[1], args[2]))
            user = UserController.reg(args[0], args[1], args[2])
            user_view.success_reg(user)
            LOGGER.info("Пользователь {} успешно зарегистрирован\r\n\r\n".format(user.username))
    elif subcategory == SubCategories.edit:
        if len(args) != 4:
            LOGGER.error("Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".
                         format(4, len(args)))
            user_view.edit_format()
        else:
            if args[0] == 'name':
                try:
                    user, oldname = UserController.edit(args[1], args[2], args[0], args[3])
                    LOGGER.info("Пробуем изменить имя пользователя для {}".format(user.username))
                    UserStorage.set_username_for_user(user, oldname)
                    LOGGER.info("Имя пользователя успешно изменено\r\n\n\n")
                    user_view.username_edit()
                except:
                    print(user_view.failed())
            elif args[0] == 'password':
                try:
                    user, oldname = UserController.edit(args[1], args[2], args[0], args[3])
                    LOGGER.info("Пробуем изменить пароль пользователя для {}".format(user.username))
                    UserStorage.set_password_for_user(user)
                    LOGGER.info("Пароль пользователя успешно изменен\r\n\n")
                    user_view.password_edit()
                except:
                    print(user_view.failed())
            else:
                user_view.edit_format()
    elif subcategory == SubCategories.delete:
        if len(args) != 0:
            incorrent_args_len()
        else:
            UserController.delete()


def parse_project(subcategory, args):
    """
    Обработчик для "Проект"
    :param subcategory:
    :param args:
    :return:
    """
    if subcategory == SubCategories.add:
        if len(args) != 4:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(4, len(args)))
            project_view.add_format()
        else:
            LOGGER.info("Попытка создать проект с названием {} и описанием".format(args[2],args[3]))
            project = ProjectController.create(args[0], args[1], args[2], args[3])
            project_view.success_create(project)
            LOGGER.info("Проект {} был успешно создан".format(args[2]))
    elif subcategory == SubCategories.delete:
        if len(args) != 3:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(3, len(args)))
            delete_format()
        else:
            LOGGER.info("Попытка удалить проект {}".format(args[2]))
            ProjectController.delete(args[0], args[1], args[2])
            LOGGER.info("Проект с названием {} был удалён\r\n\r\n".format(args[2]))
            project_view.success_delete()
    elif subcategory == SubCategories.show:
        if len(args) != 3:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(3, len(args)))
            incorrent_args_len()
        else:
            if args[0] == 'all':
                LOGGER.info("Попытка вывести список всех проектов для текущего пользователя")
                projects = ProjectController.show_all(args[1], args[2])
                LOGGER.info("Был выведен список всех проектов")
                project_view.show_info(projects)
    elif subcategory == SubCategories.edit:
        if len(args) != 5:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(5, len(args)))
            project_view.edit_format()
        else:
            if args[0] == 'name':
                LOGGER.info("Попытка изменить название проекта {}".format(args[3]))
                ProjectController.edit_name(args[1], args[2], args[3], args[4])
                LOGGER.info("Проект был успешно изменен")
            if args[0] == 'description' or 'desc':
                LOGGER.info("Попытка изменить название проекта {}".format(args[3]))
                ProjectController.edit_description(args[1], args[2], args[3], args[4])
                LOGGER.info("Проект был успешно изменен")
            else:
                print(project_view.edit_format())
    elif subcategory == SubCategories.members:
        if len(args) != 5:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(5, len(args)))
            incorrent_args_len()
        else:
            if args[0] == 'add':
                LOGGER.info("Попытка добавить {} в проект {}")
                ProjectController.add_person_to_project(args[1], args[2], args[3], args[4])
            elif args[0] == 'delete':
                ProjectController.delete_person_from_project(args[1], args[2], args[3], args[4])


def parse_column(subcategory, args):
    """
    Обработчик для для "Колонка"
    :param subcategory:
    :param args:
    :return:
    """
    if subcategory == SubCategories.add:
        if len(args) != 5:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(5, len(args)))
            column_view.create_format()
        else:
            ColumnController.create_columm(args[0], args[1], args[2], args[3], args[4])
            column_view.success_create()
    if subcategory == SubCategories.delete:
        if len(args) != 3:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(3, len(args)))
            incorrent_args_len()
        else:
            if ColumnController.delete_column(args[0], args[1], args[2], args[3]) == 0:
                column_view.success_delete()
    if subcategory == SubCategories.edit:
        if len(args) != 6:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(6, len(args)))
            incorrent_args_len()
        else:
            if args[0] == 'name':
                ColumnController.edit_name(args[1], args[2], args[3], args[4], args[5])
                column_view.success_edit()
            elif args[0] == 'description' or 'desc':
                ColumnController.edit_desc(args[1], args[2], args[3], args[4], args[5])
                column_view.success_edit()
    if subcategory == SubCategories.show:
        if len(args) != 4:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(4, len(args)))
            column_view.show_format()
        else:
            if args[0] == 'all':
                cols = ColumnController.show_all(args[1], args[2], args[3])
                column_view.show_all(cols)


def parse_task(subcategory, args):
    """
    Обработчик для "Задача"
    :param subcategory:
    :param args:
    :return:
    """
    if subcategory == SubCategories.add:
        if len(args) != 10:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(10, len(args)))
            TaskView.create_format()
        else:
            task = TaskController.add_task(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7],
                                           args[8], args[9])
            TaskView.success_create(task)
    if subcategory == SubCategories.show:
        if args[0] == 'all':
            tasks = TaskController.show_tasks(args[1], args[2], args[3], args[4])
            TaskView.show_tasks(tasks)
    if subcategory == SubCategories.delete:
        if len(args) != 5:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(5, len(args)))
            incorrent_args_len()
        else:
            TaskController.delete_task(args[0], args[1], args[2], args[3], args[4])
    if subcategory == SubCategories.edit:
        if len(args) != 7:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(7, len(args)))
            TaskView.edit_format()
        else:
            TaskController.edit(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
            TaskView.success_edit()
    if subcategory == SubCategories.subtask:
        if args[0] == 'add':
            if len(args) != 7:
                LOGGER.error(
                    "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(4, len(args)))
                TaskView.add_subtask_format()
            else:
                TaskController.set_subtask(args[1], args[2], args[3], args[4], args[5], args[6])


def parse_regular_task(subcategory, args):
    """
    Обработчик для "Регулярная задача
    :param subcategory:
    :param args:
    :return:
    """
    if subcategory == SubCategories.add:
        if len(args) != 12:
            LOGGER.error(
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(12, len(args)))
            RegularTaskView.create_format()
        else:
            task = RegularTaskController.add_task(args[0], args[1], args[2], args[3], args[4], args[5], args[6],
                                                  args[7],
                                                  args[8], args[9], args[10], args[11])
            TaskView.success_create(task)
