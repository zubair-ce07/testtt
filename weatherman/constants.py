""" contain all coonstants """
from datetime import datetime

"""Color codes"""
CRED = '\033[91m'
CBLUE = '\033[94m'
CEND = '\033[0m'

"""Default Values"""
DEFAULT = -1000
DEFAULT_DATE = datetime.strptime("1970-01-01", '%Y-%m-%d')

"""Month array"""
FILE_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'NOV', 'DEC']
