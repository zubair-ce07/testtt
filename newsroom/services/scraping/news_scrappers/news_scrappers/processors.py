
from datetime import datetime


class CleanDate(object):
    def __call__(self, date):
        date = date[0]
        date = date.strip().strip('\r').replace(" ", "-").replace(",", "")
        date = datetime.strptime(date, '%B-%d-%Y')
        return date


class StripString(object):
    def __init__(self, separator=u' '):
        self.separator = separator

    def __call__(self, values):
        return self.separator.join(values).strip(' \r\n')


class StripStringTakeFirst(object):
    def __call__(self, values):
        for value in values:
            string = value.strip(' \r\n')
            if string:
                return string
        return 'un-identified'


class StripURL(object):
    def __call__(self, values):
        return values[0].strip(' \r\n')
