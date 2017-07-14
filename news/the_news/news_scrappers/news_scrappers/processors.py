__author__ = 'luqman'


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
        string = string.strip(' \r\n').strip('\r')
        return string.encode('utf-8')