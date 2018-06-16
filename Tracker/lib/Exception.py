# Объединить эксепшены по группам

class BaseException(Exception):
    pass

class ProjectWithThisNameAlreadyExist(BaseException):
    def __init__(self):
        super().__init__("Проект с таким именем уже существует")


class UserAlreadyExist(BaseException):
    def __init__(self):
        super().__init__("Пользователь с таким именем уже зарегистрирован")


class AlreadyInArchive(BaseException):
    def __init__(self):
        super().__init__("Данная задача уже находится в архиве")


class IncorrentPassword(BaseException):
    def __init__(self):
        super().__init__("Неправильный пароль")


class CannotGetProject(BaseException):
    def __init__(self):
        super().__init__("Невозможно получить проект с указанным названием")


class UAreNotAdmin(BaseException):
    def __init__(self):
        super().__init__("Вы не являетесь создателем данного проекта")

class NoPermission(BaseException):
    def __init__(self):
        super().__init__("У вас нет прав доступа к этому проекту")


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