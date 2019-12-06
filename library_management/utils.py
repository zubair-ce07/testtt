from rest_framework.serializers import ValidationError

from constants import AUTHOR, PUBLISHER


def validate_password(password, password2):
    """ This method checks if given password are equal"""
    if password != password2:
        raise ValidationError({'password': 'Passwords must match.'})

    return True


def regisiter_user(data, model_klass):
    """This method creates and returns the user with given data"""
    if model_klass.__name__ == AUTHOR:
        user = model_klass(username=data['username'],
                           first_name=data['first_name'])
    elif model_klass.__name__ == PUBLISHER:
        user = model_klass(username=data['username'],
                           company_name=data['company_name'])
    else:
        return None

    validate_password(data['password'], data['password2'])
    user.set_password(data['password'])
    user.save()
    return user


def list_intersection(list1, list2):
    """
    This method return the List of common items from the given lists
    It uses set for processing, so duplicates are are removed
    """
    return list(set(list1) & set(list2))


def list_diff(list1, list2):
    """
    This method returns List from list1 without elements from lis2.
    It uses set for processing, so duplicate sare are removed
    """
    return list(set(list1) - set(list2))
