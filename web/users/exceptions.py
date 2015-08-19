

class EmailAlreadyExists(Exception):
    message = 'This email already exists.'


class PasswordTooShort(Exception):
    message = 'Password is too short.'


class MustContainSpecialCharacter(Exception):
    message = 'Password must contain at least one special character.'

