class MyProjectBaseException(Exception):
    pass
# переименовать

class UserException(BaseException):
    pass


class UserAlreadyExist(UserException):
    def __init__(self):
        super().__init__("A user with this name is already registered")


class IncorrentPassword(UserException):
    def __init__(self):
        super().__init__("Incorrect password")


class ProjectException(BaseException):
    pass


class NoProjectWithThisName(ProjectException):
    def __init__(self):
        super().__init__("There is no project with this name")


class ProjectWithThisNameAlreadyExist(ProjectException):
    def __init__(self):
        super().__init__("Project with this name is already exist")


class ProjectIsNotExist(ProjectException):
    def __init__(self):
        super().__init__("Project is not exist")


class NoPermission(ProjectException):
    def __init__(self):
        super().__init__("You do not have access to this project")


class UAreNotAdmin(ProjectException):
    def __init__(self):
        super().__init__("You are not the Creator of this project")


class UserAlreadyExistInProject(ProjectException):
    def __init__(self):
        super().__init__("This user is already exist in this project")


class UserIsNotExistInProject(ProjectException):
    def __init__(self):
        super().__init__("User is not already exist in this project")


class CannotDeleteCreator(ProjectException):
    def __init__(self):
        super().__init__("You can't delete creator of project")


class ColumnException(BaseException):
    pass


class NoColumnWithThisName(ProjectException):
    def __init__(self):
        super().__init__("There is no column with this name")


class ColumnWithThisNameAlreadyExist(BaseException):
    def __init__(self):
        super().__init__("Column with this name is already exist")


class TaskException(BaseException):
    pass


class AlreadyInArchive(BaseException):
    def __init__(self):
        super().__init__("Данная задача уже находится в архиве")


class CannotGetProject(BaseException):
    def __init__(self):
        super().__init__("Невозможно получить проект с указанным названием")


class NoUser(BaseException):
    def __init__(self):
        super().__init__("Не существует пользователя с таким именем")


class TaskWithThisNameAlreadyExist(BaseException):
    def __init__(self, name):
        super().__init__("Задача с названием {} уже существует в выбранной колонке".format(name))


class NotDate(BaseException):
    def __init__(self):
        super().__init__("Введенная дата не совпадает с требуемым форматом")


class EndBeforeStart(BaseException):
    def __init__(self):
        super().__init__("Указанная дата окончания задачи идет до даты начала задачи")


class StartBeforeToday(BaseException):
    def __init__(self):
        super().__init__("Задача не может быть начата до сегодняшнего дня")


class NoTask(BaseException):
    def __init__(self):
        super().__init__("Невозможно найти задачу с таким названием")


class XXXXXX(Exception):
    def __init__(self):
        super().__init__("ЭксЭксЭксТентасьон")


class SubtaskDateException(BaseException):
    def __init__(self):
        super().__init__("Временные границы подзадачи должны входить во временные границы родительской задачи")


class SubtaskPriorityException(BaseException):
    def __init__(self):
        super().__init__("Приоритет подзадачи не может быть выше приоритета родительской задачи")


class AlreadySubtask(BaseException):
    def __init__(self):
        super().__init__("Данная задача уже является подзадачей")


class CanNotDeleteBecauseSubtasks(BaseException):
    def __init__(self):
        super().__init__("Невозможно удалить задачу, пока не завершены все подзадачи")


class TypeErro(BaseException):
    def __init__(self):
        super().__init__("Ошибка приведения типов")


class ThereIsNoSuchCategory(BaseException):
    def __init__(self):
        super().__init__("Такой категории команд не существует")


class ThereIsNoSuchSubcategory(BaseException):
    def __init__(self):
        super().__init__("Нет такой команды")
