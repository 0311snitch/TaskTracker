from enum import Enum

import os

import Tracker.console.presentations.Column as column_view
import Tracker.console.presentations.User as user_view
import Tracker.console.presentations.Project as project_view
from Tracker.console.presentations.Project import *
from Tracker.console.presentations.RegularTask import *
from Tracker.console.presentations.Task import *
from Tracker.lib import conf
from Tracker.lib.controllers.Column import *
from Tracker.lib.controllers.Project import *
from Tracker.lib.controllers.RegularTask import *
from Tracker.lib.controllers.Task import *
from Tracker.lib.controllers.User import *
from Tracker.lib.storage_controller.Task import *
from Tracker.lib.storage_controller.User import *
import Tracker.lib.logger as logger
import Tracker.console.config as config


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
    try:
        return Categories[arg]
    except:
        raise ThereIsNoSuchCategory


def set_subcategory(arg):
    try:
        return SubCategories[arg]
    except:
        raise ThereIsNoSuchSubcategory


def incorrent_args_len():
    print('Некорректное количество аргументов. Для получения информации о командах введите help')


def no_category():
    print("Не было введено ни одной команды. Для просмотра возможных команд воспользуйтесь командой help")


def no_subcategory():
    print("Не была введена подкоманда. Для просмотра возможных подкоманд введите 'команда' help")


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

def check_db_exists(path):

    config.check_tracker_folder(path)
    path_to_db = os.path.join(path, 'database.sqlite3')
    #if not os.path.exists(path_to_db):
     #   ControlTask.create_tables(path_to_db)
      #  ControlPlan.create_tables(path_to_db)
       # ControlUser.create_tables(path_to_db)
        #ControlProject.create_tables(path_to_db)
        #ControlNotif.create_tables(path_to_db)


def parse(args):
    """
    The point of entry to the program, where it is determined which handler is needed.
    :param args:
    :return:
    """
    log_tag = "parser"
    log = logger.get_logger(log_tag)
    count = len(args)
    check_db_exists(conf.get_path_to_db())
    path = conf.get_path_to_db()
    path = os.path.join(path, 'database.sqlite3')
    if count == 0:
        no_category()
        log.error('Incorrect number of arguments')
    elif count == 1:
        no_subcategory()
        log.error("No subcommand")
    else:
        try:
            category = set_category(args[0])
            subcategory = set_subcategory(args[1])
            log.info("List of arguments : {}".format(args))

            if category == Categories.user:
                parse_user(subcategory, args[2:])
            if category == Categories.project:
                if len(args) > 4:
                    check_notifications(args[3], args[4])
                parse_project(subcategory, args[2:])
            elif category == Categories.column:
                if len(args) > 4:
                    check_notifications(args[2], args[3])
                parse_column(subcategory, args[2:])
            elif category == Categories.task:
                if len(args) > 4:
                    check_notifications(args[2], args[3])
                parse_task(subcategory, args[2:])
            elif category == Categories.regular_task:
                if len(args) > 4:
                    check_notifications(args[2], args[3])
                parse_regular_task(subcategory, args[2:])
        except BaseException as error:
            log.error(error)
            print(error)


def parse_user(subcategory, args):
    """
    "User" handler
    :param subcategory:
    :param args:
    :return:
    """
    log_tag = "parse_user"
    log = logger.get_logger(log_tag)
    if subcategory == SubCategories.register:
        if len(args) != 3:
            log.error(
                "Incorrect number of arguments. Expected {} , but {} was recieved".format(3, len(args)))
            user_view.reg_format()
        else:
            log.info("Attempt to register a user with a name - {}, password -  {} and e-mail - {}"
                     .format(args[0], args[1], args[2]))
            user = UserController.reg(args[0], args[1], args[2])
            user_view.success_reg(user)
            log.info("User {} successfully registered".format(user.username))
    elif subcategory == SubCategories.edit:
        if len(args) != 4:
            log.error("Incorrect number of arguments. Expected {}, but {} was recieved".format(4, len(args)))
            user_view.edit_format()
        else:
            if args[0] == 'name':
                UserController.edit(args[1], args[2], args[0], args[3])
                log.info("Trying to change the name for {}".format(args[1]))
                log.info("Username is successfully changed")
                user_view.username_edit()
            elif args[0] == 'password':
                UserController.edit(args[1], args[2], args[0], args[3])
                log.info("Trying to change the password for {}".format(args[1]))
                log.info("Password is successfully changed")
                user_view.password_edit()
            else:
                user_view.edit_format()
    elif subcategory == SubCategories.delete:
        if len(args) != 2:
            user_view.delete_fotmat()
        else:
            log.info("Trying to delete a user")
            UserController.delete(args[0], args[1])
            log.info("User is successfully deleted")
            user_view.success_delete()


def parse_project(subcategory, args):
    """
    "Project" handler
    :param subcategory:
    :param args:
    :return:
    """
    log_tag = "parse_project"
    log = logger.get_logger(log_tag)
    if subcategory == SubCategories.add:
        if len(args) != 4:
            log.error("Incorrect number of arguments. Expected {} , but {} was recieved".format(4, len(args)))
            project_view.add_format()
        else:
            log.info("Trying to create a project with the name - {} and description - {}".format(args[2], args[3]))
            project = ProjectController.create(args[0], args[1], args[2], args[3])
            project_view.success_create(project)
            log.info("Project {} was successfully created".format(args[2]))
    elif subcategory == SubCategories.delete:
        if len(args) != 3:
            log.error("Incorrect number of arguments. Expected {}, but {} was recieved".format(3, len(args)))
            delete_format()
        else:
            log.info("Trying to delete a project {}".format(args[2]))
            ProjectController.delete(args[0], args[1], args[2])
            project_view.success_delete()
            log.info("Project {} is successfully deleted".format(args[2]))
    elif subcategory == SubCategories.show:
        if len(args) != 3:
            incorrent_args_len()
            log.error("Incorrect number of arguments. Expected {} , but {} was recieved".format(4, len(args)))
        else:
            if args[0] == 'all':
                log.info("Trying to show all projects of this user")
                projects = ProjectController.show_all(args[1], args[2])
                project_view.show_info(projects)
                log.info("All project was shown")
    elif subcategory == SubCategories.edit:
        if len(args) != 5:
            project_view.edit_format()
            log.error("Incorrect number of arguments. Expected {} , but {} was recieved".format(4, len(args)))
        else:
            if args[0] == 'name':
                log.info("Trying to change the name of '{}' project".format(args[3]))
                ProjectController.edit_name(args[1], args[2], args[3], args[4])
                project_view.success_edit()
                log.info("Project is successfully edited")
            if args[0] == 'description' or 'desc':
                log.info("Trying to change the description of  '{}' project".format(args[3]))
                ProjectController.edit_description(args[1], args[2], args[3], args[4])
                project_view.success_edit()
                log.info("Project is successfully edited")
            else:
                print(project_view.edit_format())
                log.error("Incorrect format")
    elif subcategory == SubCategories.members:
        if len(args) != 5:
            members_add_format()
            log.error("Incorrect number of arguments. Expected {} , but {} was recieved".format(4, len(args)))
        else:
            if args[0] == 'add':
                log.info("Trying to add {} to '{}' project".format(args[4], args[3]))
                ProjectController.add_person_to_project(args[1], args[2], args[3], args[4])
                log.info("User is successfully added to the project")
                project_view.user_added()
            elif args[0] == 'delete':
                ProjectController.delete_person_from_project(args[1], args[2], args[3], args[4])
                log.info(("Trying to delete {} from '{}' project".format(args[3], args[4])))
                log.info("User is successfully deleted from project")
                project_view.user_deleted()
            else:
                members_add_format()


def parse_column(subcategory, args):
    """
    "Column" handler
    :param subcategory:
    :param args:
    :return:
    """
    log_tag = "parse_column"
    log = logger.get_logger(log_tag)
    if subcategory == SubCategories.add:
        if len(args) != 5:
            log.error("Incorrect number of arguments. Expected {} , but {} was recieved".format(5, len(args)))
            column_view.create_format()
        else:
            log.info("Trying to create a column with the name - {} and description - {}".format(args[3], args[4]))
            ColumnController.create_columm(args[0], args[1], args[2], args[3], args[4])
            column_view.success_create()
            log.info("Column {} was successfully created".format(args[3]))
    if subcategory == SubCategories.delete:
        if len(args) != 4:
            log.error("Incorrect number of arguments. Expected {} , but {} was recieved".format(3, len(args)))
            column_view.delete_format()
        else:
            log.info("Trying to delete a column with the name - {} and description - {}".format(args[3], args[4]))
            ColumnController.delete_column(args[0], args[1], args[2], args[3])
            column_view.success_delete()
            log.info("Column {} was successfully deleted".format(args[3]))
    if subcategory == SubCategories.edit:
        if len(args) != 6:
            log.error("Incorrect number of arguments. Expected {} , but {} was recieved".format(6, len(args)))
        else:
            log.info("Trying to edit a column with the name - {} and description - {}".format(args[3], args[4]))
            if args[0] == 'name':
                ColumnController.edit_name(args[1], args[2], args[3], args[4], args[5])
                column_view.success_edit()
                log.info("Column {} is successfully edited. New name is {}".format(args[4],args[5]))
            elif args[0] == 'description' or 'desc':
                ColumnController.edit_desc(args[1], args[2], args[3], args[4], args[5])
                column_view.success_edit()
                log.info("Column {} is successfully edited. New description is {}".format(args[4], args[5]))
            else:
                log.error("Incorrect format")
    if subcategory == SubCategories.show:
        if len(args) != 4:
            log.error("Incorrect number of arguments. Expected {} , but {} was recieved".format(4, len(args)))
            column_view.show_format()
        else:
            if args[3] == 'all':
                log.info("Trying to show a column with the name - {} and description - {}".format(args[3], args[4]))
                cols = ColumnController.show_all(args[0], args[1], args[2])
                column_view.show_all(cols)
                log.info("All columns was shown")


def parse_task(subcategory, args):
    """
    "Task" handler
    :param subcategory:
    :param args:
    :return:
    """
    log_tag = "parse_task"
    log = logger.get_logger(log_tag)
    if subcategory == SubCategories.add:
        if len(args) != 10:
            log.error("Incorrect number of arguments. Expected {} , but {} was recieved".format(10, len(args)))
            TaskView.create_format()
        else:
            log.info("Trying to add task with the name - {}".format(args[4]))
            task = TaskController.add_task(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7],
                                           args[8], args[9])
            TaskView.success_create(task)
            log.info("Task is successfully added")
    if subcategory == SubCategories.show:
        if args[0] == 'all':
            log.info("Trying to show all tasks in this column of project")
            tasks = TaskController.show_tasks(args[1], args[2], args[3], args[4])
            TaskView.show_tasks(tasks)
            log.info("All task was shown")
    if subcategory == SubCategories.delete:
        if len(args) != 5:
            log.error("Incorrect number of arguments. Expected {} , but {} was recieved".format(5, len(args)))
            incorrent_args_len()
        else:
            log.info("Trying to delete task")
            TaskController.delete_task(args[0], args[1], args[2], args[3], args[4])
            log.info("Task is successfully deleted")
    if subcategory == SubCategories.edit:
        if len(args) != 7:
            log.error("Incorrect number of arguments. Expected {} , but {} was recieved".format(7, len(args)))
            TaskView.edit_format()
        else:
            log.info("Tring to edit a column")
            TaskController.edit(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
            TaskView.success_edit()
            log.info("Task is successfully edited")
    if subcategory == SubCategories.subtask:
        if args[0] == 'add':
            if len(args) != 7:
                log.error("Incorrect number of arguments. Expected {} , but {} was recieved".format(4, len(args)))
                TaskView.add_subtask_format()
            else:
                log.info("Trying to set subtask to task")
                TaskController.set_subtask(args[1], args[2], args[3], args[4], args[5], args[6])
                log.info("Task is successfully set as subtask")


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
                "Было введено неправильное количество аргументв. Ожидалось {} , было получено {}\r\n\r\n".format(12,
                                                                                                                 len(
                                                                                                                     args)))
            RegularTaskView.create_format()
        else:
            task = RegularTaskController.add_task(args[0], args[1], args[2], args[3], args[4], args[5], args[6],
                                                  args[7],
                                                  args[8], args[9], args[10], args[11])
            TaskView.success_create(task)
