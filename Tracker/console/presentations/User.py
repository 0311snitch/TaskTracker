def success_reg(user):
    print("Регистрация успешно завершена.\n\nВаш логин- {}\nВаш пароль - {}\nВаш email - {}\nВаш token - {}\n".format(
        user.username,
        user.password,
        user.email, user.token))


def welcome_back(username):
    print("Вы успешно авторизовались, {}. Теперь можно начать работу с приложением.".format(username))


def no_user():
    print("Такого пользователя нет в базе данных")


def failed():
    print("Не удалось завершить выполнение команды.")


def logout_error():
    print("Пользватель не был заранее авторизован.")


def need_logout():
    print("Пользователь уже авторизован. Для авторизации другого пользователя сперва необходимо выйти из аккаунта при "
          "помощи команды logout")


def seeu():
    print("Вы вышли из аккаунта")


def reg_format():
    print(
        "Для регистрации пользователя необходимо ввести команду в формате :\n user register 'username' 'password' "
        "'email'")


def login_format():
    print("Для авторизации пользователя необходимо ввести команду в формате : user login 'username' 'password'")

def invalid_password():
    print("Был введен некорректный пароль")


def create_error():
    print("Ошибка создания проекта")

def u_are_not_admin():
    print("Вы не являетесь создателем этого проекта")

def no_such():
    print("Такого пользователя нет в проекте")

def username_edit():
    print("Имя пользователя было успешно изменено")

def password_edit():
    print("Пароль пользователя был успешно изменен")

def edit_format():
    print("Для изменения пользователя необходимо ввести команду в формате :\n user edit 'name/password' 'username' 'password' 'new value'")

def no_permission():
    print("Вы не являетесь создателем этого проекта. Изменять проект может только создатель")