def success_create(project):
    print("\n\nПроект успешно создан.\nНазвание - {}\nОписание - {}\n\n".format(project.name, project. description))

def success_delete():
    print("Проект был успешно удален")

def failed():
    print("Проект с таким названием уже есть. Выберите существующий проект или удалите проект для создания нового.")

def need_user():
    print("Для того, чтобы создать новый проект необходимо сначала авторизоваться")

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