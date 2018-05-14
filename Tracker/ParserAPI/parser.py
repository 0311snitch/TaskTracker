from Tracker.models.Project import *
from enum import Enum
from Tracker.models.User import *


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


def set_category(arg):
    return Categories[arg]

def set_subcategory(arg):
    return SubCategories[arg]

def incorrent_args_len():
    print('Некорректное количество аргументов. Для получения информации о командах введите help')

def parse(args):
    print(args)
    count = len(args)
    if count == 0:
        incorrent_args_len()
    else:
        category = set_category(args[0])
        subcategory = set_subcategory(args[1])
        print(category)
        if category == Categories.user:
            if subcategory == SubCategories.register:
                if len(args) != 5:
                    incorrent_args_len()
                else:
                    User.reg(args[2], args[3], args[4])
            elif subcategory == SubCategories.login:
                if len(args) != 4:
                    incorrent_args_len()
                else:
                    User.login(args[2], args[3])
            elif subcategory == SubCategories.logout:
                if len(args) != 2:
                    incorrent_args_len()
                else:
                    User.logout()
        elif category == Categories.project:
            if subcategory == SubCategories.add:
                if len(args) != 4:
                    incorrent_args_len()
                else:
                    Project.create(args[2],args[3])
            elif subcategory == SubCategories.show:
                if args[2] == 'all':
                    if len(args) != 3:
                        incorrent_args_len()
                    else:
                        Project.show_all()
            elif subcategory == SubCategories.delete:
                if len(args) != 3:
                    incorrent_args_len()
                else:
                    Project.delete(args[2])
            elif subcategory == SubCategories.select:
                if len(args) != 3:
                    incorrent_args_len()
                else:
                    Project.select(args[2])
            elif subcategory == SubCategories.edit:
                if len(args) != 5:
                    incorrent_args_len()
                else:
                    if args[2] == 'name':
                        Project.edit_name(args[3], args[4])

