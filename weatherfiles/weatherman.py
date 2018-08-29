import sys
import calendar

from DataParser import DataParser
from Computer import Computer

data = {
    'Features': [],
    'values': []
}

directory = sys.argv[1]
var = sys.argv[2:]

# Collecting data
data = DataParser.parsefile(directory, data)

for index in range(len(var) - 1):
    if index % 2 == 0:
        action = var[index]
        date = var[index + 1]
        result = {}
        date = date.replace('/0', '/')

        if action == '-e':
            result = Computer.compute_e(data, date)
            print(
                'Highest: ' + result['Highest'] + '\n' +
                'Lowest: ' + result['Lowest'] + '\n' +
                'Humidity: ' + result['Humidity'] + '\n'
            )
        elif action == '-a':
            result = Computer.compute_a(data, date)
            print(
                'Highest Average: ' + result['Highest Average'] + '\n' +
                'Lowest Average: ' + result['Lowest Average'] + '\n' +
                'Average Mean Humidity: ' + result['Average Mean Humidity'] + '\n'
            )
        elif action == '-c':
            result = Computer.compute_c(data, date)
            year, month = date.split('/')

            print(calendar.month_name[int(month)] + ' ' + year)

            for key, value in sorted(result.items()):
                sign, temp = value[0].split(' ')
                print(key + ' \033[1;31m' + sign + '\033[m ' + temp)

                sign, temp = value[1].split(' ')
                print(key + ' \033[1;34m' + sign + '\033[m ' + temp)

            print('Bonus')

            for key, value in sorted(result.items()):
                signhigh, temphigh = value[0].split(' ')
                signlow, templow = value[1].split(' ')
                print(key + ' \033[1;34m' + signlow + '\033[1;31m' + signhigh + '\033[m ' + templow + ' - ' + temphigh)
