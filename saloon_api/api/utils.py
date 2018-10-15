"""
Contains saome helper functions.
"""

import random
import string


def get_random_string():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
