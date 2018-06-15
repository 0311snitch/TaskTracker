from enum import Enum
from Tracker.controllers.User import *
from Tracker.controllers.Project import *
from Tracker.presentations.Column import *
from Tracker.presentations.Task import *
from Tracker.controllers.Column import *
from Tracker.controllers.Task import *


class Categories(Enum):
    user = 0
    project = 1
    column = 2
    task = 3
    repeatedtask = 4
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


def parse(args):
    # print(args)
    count = len(args)
    if count == 0:
        incorrent_args_len()
    else:
        try:
            category = set_category(args[0])
            subcategory = set_subcategory(args[1])
            # print(category)
            if category == Categories.user:
                parse_user(subcategory, args[2:])
            elif category == Categories.project:
                parse_project(subcategory, args[2:])
            elif category == Categories.column:
                parse_column(subcategory, args[2:])
            elif category == Categories.task:
                parse_task(subcategory, args[2:])
        except:
            pass


def parse_user(subcategory, args):
    if subcategory == SubCategories.register:
        if len(args) != 3:
            user_view.reg_format()
        else:
            user = UserController.reg(args[0], args[1], args[2])
            user_view.success_reg(user)
    elif subcategory == SubCategories.edit:
        if len(args) != 4:
            user_view.edit_format()
        else:
            if args[0] == 'name':
                try:
                    user, oldname = UserController.edit(args[1], args[2], args[0], args[3])
                    UserStorage.set_username_for_user(user, oldname)
                    user_view.username_edit()
                except:
                    print(user_view.failed())
            elif args[0] == 'password':
                try:
                    user, oldname = UserController.edit(args[1], args[2], args[0], args[3])
                    UserStorage.set_password_for_user(user)
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
    if subcategory == SubCategories.add:
        if len(args) != 4:
            project_view.add_format()
        else:
            project = ProjectController.create(args[0], args[1], args[2], args[3])
            project_view.success_create(project)
    elif subcategory == SubCategories.delete:
        if len(args) != 3:
            delete_format()
        else:
            ProjectController.delete(args[0], args[1], args[2])
            project_view.success_delete()
    elif subcategory == SubCategories.show:
        if len(args) != 3:
            incorrent_args_len()
        else:
            if args[0] == 'all':
                projects = ProjectController.show_all(args[1], args[2])
                project_view.show_info(projects)
    elif subcategory == SubCategories.edit:
        if len(args) != 5:
            project_view.edit_format()
        else:
            if args[0] == 'name':
                ProjectController.edit_name(args[1], args[2], args[3], args[4])
            if args[0] == 'description' or 'desc':
                ProjectController.edit_description(args[1], args[2], args[3], args[4])
            else:
                print(project_view.edit_format())
    elif subcategory == SubCategories.members:
        if len(args) != 5:
            incorrent_args_len()
        else:
            if args[0] == 'add':
                ProjectController.add_person_to_project(args[1], args[2], args[3], args[4])
            elif args[0] == 'delete':
                ProjectController.delete_person_from_project(args[1], args[2], args[3], args[4])


def parse_column(subcategory, args):
    if subcategory == SubCategories.add:
        if len(args) != 5:
            create_format()
        else:
            ColumnController.create_columm(args[0], args[1], args[2], args[3], args[4])
            column_view.success_create()
    if subcategory == SubCategories.delete:
        if len(args) != 3:
            incorrent_args_len()
        else:
            if ColumnController.delete_column(args[0], args[1], args[2], args[3]) == 0:
                column_view.success_delete()
    if subcategory == SubCategories.edit:
        if len(args) != 6:
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
            show_format()
        else:
            if args[0] == 'all':
                cols = ColumnController.show_all(args[1], args[2], args[3])
                show_all(cols)


def parse_task(subcategory, args):
    if subcategory == SubCategories.add:
        if len(args) != 11:
            TaskView.create_format()
        else:
            TaskController.add_task(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8],
                                    args[9], args[10])
    if subcategory == SubCategories.show:
        if args[0] == 'all':
            tasks = TaskController.show_tasks(args[1],args[2],args[3],args[4])
            TaskView.show_tasks(tasks)
    if subcategory == SubCategories.delete:
        if len(args) != 5:
            incorrent_args_len()
        else:
            TaskController.delete_task(args[0],args[1],args[2],args[3],args[4])
    if subcategory == SubCategories.edit:
        if len(args) != 7:
            TaskView.edit_format()
        else:
            TaskController.edit(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
            TaskView.success_edit()
    if subcategory == SubCategories.subtask:
        if args[0] == 'add':
            if len(args) != 7:
                TaskView.add_subtask_format()
            else:
                TaskController.set_subtask(args[1], args[2], args[3], args[4], args[5], args[6])
        if args[0] == 'get':
            TaskStorage.get_all_subtasks(args[1],args[2],TaskStorage.get_task('Project337','NewColumn','FirstTask1'))
