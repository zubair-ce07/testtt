import datetime


class CPrinter:

    W = '\033[0m'
    R = '\033[31m'
    G = '\033[32m'

    def yprint(self, records):
        mxtemp, mintemp, mxhumid = tuple(records)
        time, max, min, humid = mxtemp
        print ('Highest: ' + max + 'C on ' + datetime.datetime.strptime(time, '%Y-%m-%d').strftime('%B %d'))
        time, max, min, humid = mintemp
        print ('Lowest: ' + min + 'C on ' + datetime.datetime.strptime(time, '%Y-%m-%d').strftime('%B %d'))
        time, max, min, humid = mxhumid
        print ('Humid: ' + humid + 'C on ' + datetime.datetime.strptime(time, '%Y-%m-%d').strftime('%B %d'))

    def mprint(self, records):
        avmtemp, avmintemp, avhumid = records
        print ('Highest Average: ' + str(avmtemp) + 'C')
        print ('Lowest: ' + str(avmintemp) + 'C')
        print ('Humid: ' + str(avhumid) + 'C')

    def cprint(self, records):
        date, _, _, _ = records[0]
        print (datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%B %Y'))
        for row in records:
            date, mxtemp, mintemp, _ = row
            _, date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%B %d').split(' ')
            print (date + ' ' + self.R + int(mxtemp)*'+' + self.W + ' ' + mxtemp + 'C')
            print (date + ' ' + self.G + int(mintemp)*'+' + self.W + ' ' + mintemp + 'C')

    def csprint(self, records):
        date, _, _, _ = records[0]
        print (datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%B %Y'))
        for row in records:
            date, mxtemp, mintemp, _ = row
            _, date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%B %d').split(' ')
            print (date + ' ' + self.R + int(mxtemp) * '+' + self.G + int(mintemp) * '+' + self.W + ' ' + mxtemp + '-' + mintemp + 'C')