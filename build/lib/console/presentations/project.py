def success_create(project):
    print("\n\nProject is successfully created.\nTitle - {}\nDescription - {}\n\n".format(project.name,
                                                                                          project.description))


def add_format():
    print("Wrong format. To add a project, enter a command like project add 'username' 'password' 'project name' "
          "'description of project'")


def members_add_format():
    print("Wrong format. To add a user to the project, enter a command like project members add/delete 'username' "
          "'password  'project name' 'user to add'")


def user_added():
    print("User is successfully added to project")


def user_deleted():
    print("User is successfully deleted from project")


def delete_format():
    print(
        "Wrong format. To delete a project, enter a command like project delete 'username' 'password' 'project name'")


def success_delete():
    print("Project is successfully deleted")


def show_info(project_list):
    print("Information about projects:\n")
    for i in project_list:
        print("Name - {}\nDescription - {}\nMembers:".format(i.name, i.description))
        for i in i.members:
            print(i.username)
        print("\n")


def success_save():
    print("Project is successfully saved")


def success_edit():
    print("Project is successfully edited")


def edit_format():
    print(
        "Wrong format. To edit a project, enter a command like project edit 'name/desc' 'username' 'password' 'project name'")