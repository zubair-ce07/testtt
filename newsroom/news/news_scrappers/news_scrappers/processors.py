
from datetime import datetime


class CleanDate(object):
    def __call__(self, date):
        date = date[0]
        date = date.strip().strip('\r').replace(" ", "-").replace(",", "")
        date = datetime.strptime(date, '%B-%d-%Y')
        return date


class StripString(object):
    def __call__(self, values):
        string = ' '.join(values)
        string = string.strip(' \r\n')
        return string


class StripStringTakeFirst(object):
    def __call__(self, values):
        for value in values:
            string = value.strip(' \r\n')
            if string:
                return string
        return 'no value against css'


class StripURL(object):
    def __call__(self, values):
        return values[0].strip(' \r\n')
