from functools import wraps

from flask_jwt_extended import get_jwt_identity

from asiangames.models import User


def required_access_level(access_level):
    def main_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user_email = get_jwt_identity()
            current_user_access_level = User.find_by_email(email=current_user_email).access_level

            if access_level <= current_user_access_level:
                return func(*args, **kwargs)

            return {'message': 'You don\'t have the right access level'}

        return wrapper
    return main_wrapper
