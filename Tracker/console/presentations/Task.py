class TaskView:
    @staticmethod
    def create_format():
        print("Для создания задачи необходимо ввести команду в виде task add 'username' 'password' 'project name' 'column "
              "name' 'task name' 'description' 'first date' 'second date' 'tags' 'priority'")

    @staticmethod
    def add_subtask_format():
        print("Для добавления подзадачи необходимо ввести команду в виде task subtask add 'username' 'password' "
              "'project name' 'column name' 'first task' 'second task'")

    @staticmethod
    def edit_format():
        print("Для изменения задачи необходимо ввести команду в виде tadk edit 'name/desc/tags/priority' 'username' "
              "'password' 'project name' 'column name' 'task name' 'new value")

    @staticmethod
    def show_tasks(tasks):
        print("Информация о текущих задачах:\n")
        for i in tasks:
            print("Название  - {}\nОписание - {}\nДата начала - {}\nДата завершения - {}\nТеги - {}\nПриоритет - "
                  "{}\n".format(i.name, i.desc, i.first_date, i.second_date, i.tags, i.priority))

    @staticmethod
    def success_create(i):
        print("Задача была успешно создана")
        print("Название  - {}\nОписание - {}\nДата начала - {}\nДата завершения - {}\nТеги - {}\nПриоритет - "
              "{}\n".format(i.name, i.desc, i.first_date, i.second_date, i.tags, i.priority))

    @classmethod
    def success_edit(cls):
        print("Задача была успешно изменена")