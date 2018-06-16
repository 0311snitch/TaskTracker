def success_create(project):
    print("\n\nПроект успешно создан.\nНазвание - {}\nОписание - {}\n\n".format(project.name, project.description))


def need_token():
    print("Не указан токен пользователя или неправильное количесво аргументов")


def add_format():
    print(
        "Неправильный формат. Для добавления проекта введите команду вида project add 'username' 'password' 'project name' 'description of project'")


def delete_format():
    print(
        "Неправильный формат. Для удаления проекта введите команду вида project delete 'username' 'password' 'project name'")


def success_delete():
    print("Проект был успешно удален")


def failed():
    print("Проект с таким названием уже есть. Выберите существующий проект или удалите проект для создания нового.")


def need_user():
    print("Для того, чтобы создать новый проект необходимо сначала авторизоваться")


def sucess_added_to_project():
    print("Пользователь был успешно добавлен в проект")


def project_selected(project):
    print("Вы успешно выбрали проект {}".format(project.name))


def project_already_selected():
    print("Вы пытаетесь выбрать проект, который уже является выбранным")


def show_info(project_list):
    print("Информация о проектах:\n")
    for i in project_list:
        print("Название - {}\nОписание - {}\nУчастники проекта:".format(i.name, i.description))
        for i in i.members:
            print(i.username)
        print("\n")


def success_save():
    print("Проект был успешно сохранен")


def success_edit():
    print("Проект был успешно изменен.")


def create_error():
    print("Ошибка создания проекта")


def permission_error():
    print("У вас нет доступа к этому проекту")


def delete_error():
    print("Ошибка удаления проекта")


def already_exist():
    print("Данный пользователь уже есть в проекте")


def not_exist():
    print("Такого пользователя нет в проекте")


def edit_format():
    print(
        "Для изменения проекта необходимо ввести команду в следующем формате project edit 'name/desc' 'username' 'password' 'project name'")


def cannot_delete_admin():
    print("Нельзя удалить создателя проекта")
