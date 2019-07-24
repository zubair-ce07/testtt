import csv
import sys
import os
import operator
import calendar


class WeatherMan:
    def __init__(self, path):
        self.__path = path

    def year_files(self, year):
        year_files = []
        directory_files = os.listdir(self.__path)
        for file in directory_files:
            if str(year) in file:
                year_files.append(file)
        return year_files

    def highest_record_in_a_year(self, year):
        max_temperatures = []
        low_temperatures = []
        dates = []
        max_humidities = []

        files = self.year_files(year)
        if len(files) == 0:
            print('No Data Found For This Year')
            return
        for file in files:
            with open(self.__path+file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)  # for skipping titles
                for row in csv_reader:
                    if self.check_emptinesss(row[1]):
                        max_temperatures.append(int(row[1]))
                    if self.check_emptinesss(row[3]):
                        low_temperatures.append(int(row[3]))
                    if self.check_emptinesss(row[7]):
                        max_humidities.append(int(row[7]))
                    dates.append(row[0])

        max_temperature = max(max_temperatures)
        low_temperature = min(low_temperatures)
        max_humid = max(max_humidities)

        print('Highest: '+str(max_temperature)+'C on ' +
              self.get_and_format_date(dates, max_temperatures,
                                       max_temperature))
        print('Lowest: '+str(low_temperature)+'C on ' +
              self.get_and_format_date(dates, low_temperatures,
                                       low_temperature))
        print('Humid: '+str(max_humid)+'% on ' +
              self.get_and_format_date(dates, max_humidities, max_humid))

    def check_emptinesss(self, data):
        if data == '':
            return False
        return True

    def get_and_format_date(self, date_list, data_list, data):
        date = date_list[data_list.index(data)]
        date = date.split('-')
        month = date[1]
        day = date[2]
        month = calendar.month_abbr[int(month)]
        return month + ' ' + day


report_type = sys.argv[1]
date = sys.argv[2]

months = [
    'Jan', 'Feb', 'Mar', 'Apr',
    'May', 'Jun', 'Jul', 'Aug',
    'Sep', 'Oct', 'Nov', 'Dec']

if(report_type == '-a'):
    # report_one()
    w = WeatherMan('weatherfiles//')
    w.highest_record_in_a_year(date)
