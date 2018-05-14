def success_reg(user):
    print("Регистрация успешно завершена.\n\nВаш логин- {}\nВаш пароль - {}\nВаш email - {}\n\n".format(user.username,
                                                                                                        user.password,
                                                                                                        user.email))


def welcome_back(username):
    print("Вы успешно авторизовались, {}. Теперь можно начать работу с приложением.".format(username))

def failed():
    print("Не удалось завершить выполнение команды.")

def logout_error():
    print("Пользватель не был заранее авторизован.")

def need_logout():
    print("Пользователь уже авторизован. Для авторизации другого пользователя сперва необходимо выйти из аккаунта при "
          "помощи команды logout")

def seeu():
    print("Вы вышли из аккаунта")
