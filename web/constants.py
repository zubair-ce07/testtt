
# End points' methods
METHOD_GET_LIST = {'get': 'list'}
METHOD_GET_RETRIEVE = {'get': 'retrieve'}
METHOD_PUT_UPDATE = {'put': 'update'}
METHOD_POST_CREATE = {'post': 'create'}

# Posts' validation messages
TITLE_IS_TOO_SHORT = 'Title is too short elaborate more.'
MUST_BE_NON_NEGATIVE = 'It must be non-negative.'
GIVE_VALID_TIME = 'Give valid expiry time.'

# Users' validation messages
PASSWORDS_DONT_MATCH = "Your entered passwords don't match."
PASSWORD_IS_TOO_SHORT = "Password is too short, must contain at least 8 characters."
MUST_HAVE_A_SPECIAL_CHARACTER = "Password must contain at least one special character(s)."
ENTER_CORRECT_OLD_PASSWORD = "Please enter your correct old password."

def merge(first_dict, second_dict):
    """merges two dictionaries into a third one"""
    merged_dict = second_dict.copy()
    merged_dict.update(first_dict)
    return merged_dict