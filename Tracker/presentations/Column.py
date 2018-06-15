def show_all(cols):
    print("Информация о колонках:")
    for i in cols:
        print("Навзание - {}\nОписание - {}\n".format(i.name, i.desc))


def success_create():
    print("Колонка была успешно создана")


def success_delete():
    print("Колонка была успешно удалена")


def success_select():
    print("Колонка была успешно выбрана")


def success_edit():
    print("Колонка была успешно изменена")

def create_format():
    print("Для создания колонки введите команду в формате 'username' 'password' 'project name' 'name of column' 'description of column'")

def no_permissions():
    print("Вы не являетесь создателем этого проекта")

def show_format():
    print("Для вывода всех колонок введите команду в формате 'username' 'password' 'project name' show all")