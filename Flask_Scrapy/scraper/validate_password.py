import re


def password_check(password):
    # calculating the length
    if len(password) < 8:
        return '8 characters length or more required'

    # searching for digits
    if re.search(r"\d", password) is None:
        return '1 digit or more required'

    # searching for symbols
    if re.search(r"\W", password) is None:
        return '1 symbol or more required'

    # # searching for uppercase
    # uppercase_error = re.search(r"[A-Z]", password) is None
    #
    # # searching for lowercase
    # lowercase_error = re.search(r"[a-z]", password) is None
    return None
