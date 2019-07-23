import csv
import sys
import os
import operator


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
        most_humidity = []

        files = self.year_files(year)
        if len(files) == 0:
            print('No Data Found For This Year')
            return
        for file in files:
            with open(self.__path+file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)  # for skipping titles
                for row in csv_reader:
                    if row[1] == '':
                        continue
                    max_temperatures.append(int(row[1]))
                    dates.append(row[0])
                    low_temperatures.append(int(row[3]))
                    most_humidity.append(int(row[7]))
        print('Highest: '+str(max(max_temperatures)))
        print('Lowest: '+str(min(low_temperatures)))
        print('Humid: '+str(max(most_humidity)))


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
