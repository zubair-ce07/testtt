from django.contrib.auth.models import Group


def get_group(name):
    return Group.objects.get(name=name)


def is_manager(user):
    if user.groups.first().name == 'Manager':
        return True

    return False


def is_manager_admin(user):
    if user.groups.first().name == 'ManagerAdmin':
        return True

    return False


def get_group_name(user):
    return user.groups.first().name
