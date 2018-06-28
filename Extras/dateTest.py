import datetime

b = '2001-11-1'

date = b.split('-')
a = datetime.date(int(date[0]), int(date[1]), int(date[2]))

print(a.strftime("%d %B"))

class test():
    def __init__(self):
        print('123')
        pass
