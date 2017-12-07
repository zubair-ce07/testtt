import sys
import glob
import os
import re
import calendar
from datetime import datetime
from termcolor import colored


class WeatherMan():

    def print_Yearly_results(self, file_path, year):
        file_names=[]
        os.chdir(file_path)
        for file in glob.glob("*.txt"):
            if file.find(year) != -1:
                file_names.append(file)

        if len(file_names) == 0:
            print('No File Found!')
        else:
            high_temp = {}
            low_temp = {}
            high_humidity = {}

            for file_name in file_names:
                with open(file_name, 'r') as f:
                    next(f)
                    for line in f:
                        splitted_words = line.split(',')
                        high_temp[splitted_words[0]] = splitted_words[1]
                        low_temp[splitted_words[0]] = splitted_words[3]
                        high_humidity[splitted_words[0]] = splitted_words[7]

            def key_search(x):
                return x[1]

            high_temp_res = sorted(
                high_temp.items(),
                key=key_search,
                reverse=True)
            low_temp_res = sorted(
                low_temp.items(),
                key=key_search,
                reverse=True)
            high_humidity_res = sorted(
                high_humidity.items(),
                key=key_search,
                reverse=True)

            del high_temp_res[1:]
            del low_temp_res[1:]
            del high_humidity_res[1:]
            high_date = datetime.strptime(high_temp_res[0][0], '%Y-%m-%d')
            low_date = datetime.strptime(low_temp_res[0][0], '%Y-%m-%d')
            hum_date = datetime.strptime(high_humidity_res[0][0], '%Y-%m-%d')

            print ('Highest: ' + \
                  high_temp_res[0][1] + \
                  'C on ' + \
                  high_date.strftime("%B") \
                  + ' ' + str(high_date.strftime("%d")))
            print ('Lowest: ' + low_temp_res[0][1] +\
                  'C on ' + low_date.strftime("%B") +\
                  ' ' + str(low_date.strftime("%d")))
            print ('Humidity: ' +\
                  high_humidity_res[0][1] +\
                  '% on ' + hum_date.strftime("%B") +\
                  ' ' + str(hum_date.strftime("%d")))

    def verify_directory(self, directory_path):
        return os.path.isdir(directory_path)

    def verify_year(self, year):
        return year.isdigit() and len(year) == 4

    def verify_year_month(self, year_month):
        match = re.search(r'^\d\d\d\d/\d+$', year_month)
        if match:
            splitted_words = year_month.split('/')
            month = int(splitted_words[1])
            return month >= 1 and month <= 12
        else:
            return False

    def print_month_average(self, file_path, year, month):
        file_names = []
        os.chdir(file_path)
        for file in glob.glob("*.txt"):
            if file.find(year) != -1 and file.find(month) != -1:
                file_names.append(file)

        if len(file_names) == 0:
            print('No Data Found!')
        else:
            high_temp = {}
            low_temp = {}
            high_humidity = {}

            for file_name in file_names:
                with open(file_name, 'r') as f:
                    next(f)
                    for line in f:
                        splitted_words = line.split(',')
                        high_temp[splitted_words[0]] = splitted_words[1]
                        low_temp[splitted_words[0]] = splitted_words[3]
                        high_humidity[splitted_words[0]] = splitted_words[9]

            high_temp_avg = self.find_average(high_temp.values())
            low_temp_avg = self.find_average(low_temp.values())
            high_hum_avg = self.find_average(high_humidity.values())

            print('Highest Average: ' + str(round(high_temp_avg, 2)) + 'C')
            print('Lowest average: ' + str(round(low_temp_avg, 2)) + 'C')
            print('average Mean Humidity: ' + str(round(high_hum_avg, 2)) + '%')

    def find_average(self, values):
        if len(values) != 0:
            sum_val = 0.0
            for val in values:
                if len(val) != 0:
                    sum_val += float(val)
            return sum_val / len(values)
        else:
            return 0

    def print_day_bars(self, file_path, year, month):
        file_names = []
        os.chdir(file_path)
        for file in glob.glob("*.txt"):
            if file.find(year) != -1 and file.find(month) != -1:
                file_names.append(file)

        if len(file_names) == 0:
            print('No Data Found!')
        else:
            for file_name in file_names:
                with open(file_name, 'r') as f:
                    next(f)
                    for line in f:
                        splitted_words = line.split(',')
                        day = datetime.strptime(splitted_words[0], '%Y-%m-%d')
                        high = self.get_Integer(splitted_words[1])
                        low = self.get_Integer(splitted_words[3])

                        """print(day.strftime("%d"),
                        self.print_plus(high,'red'))
                        print(str(high) + 'C')
                        print(day.strftime("%d"),
                        self.print_plus(low,'blue'))
                        print(str(low) + 'C')
                        """
                        print(day.strftime("%d"),end="")
                        self.print_plus(low, 'blue')
                        self.print_plus(high - low, 'red')
                        print(str(low) + 'C - ' + str(high) + 'C')

    def get_Integer(self, val):
        if len(val) == 0:
            result = 0
        else:
            result = int(val)
        return result

    def print_plus(self, val, color):
        i=0
        while i < val:
            print(colored('+', color),end="")
            i += 1


def sub_main(directory_path, year, report_type):
    weather = WeatherMan()
    if report_type == '-e':
        if weather.verify_directory(directory_path) and weather.verify_year(year):
            weather.print_Yearly_results(directory_path, year)
        else:
            print('Incorrect Arguments!')

    elif report_type == '-a':
        if weather.verify_directory(directory_path) and weather.verify_year_month(year):
            splitted_words = year.split('/')
            year = splitted_words[0]
            temp = calendar.month_name[int(splitted_words[1])]
            month = temp[0:3]
            weather.print_month_average(directory_path, year, month)
        else:
            print("Incorrect Arguments!")

    elif report_type == '-c':
        if weather.verify_directory(directory_path) and weather.verify_year_month(year):
            splitted_words = year.split('/')
            year = splitted_words[0]
            temp = calendar.month_name[int(splitted_words[1])]
            month = temp[0:3]
            weather.print_day_bars(directory_path, year, month)
        else:
            print("Incorrect Arguments!")


def main():
    if len(sys.argv) == 4:
        directory_path = sys.argv[1]
        year = sys.argv[3]
        report_type = sys.argv[2]
        sub_main(directory_path, year, report_type)
    elif len(sys.argv) == 8:
        directory_path = sys.argv[1]
        year1 = sys.argv[3]
        year2 = sys.argv[5]
        year3 = sys.argv[7]
        report_type1 = sys.argv[2]
        report_type2 = sys.argv[4]
        report_type3 = sys.argv[6]
        sub_main(directory_path, year1, report_type1)
        print('#########################################')
        sub_main(directory_path, year2, report_type2)
        print('#########################################')
        sub_main(directory_path, year3, report_type3)
    else:
        print('Incorrect arguments!')
    sys.exit(1)
if __name__ == '__main__':
    main()