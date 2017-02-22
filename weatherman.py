import calendar
import os
import argparse
from datetime import datetime
import csv
from termcolor import colored


class WeatherReport:
    data = []
    max_list = []
    min_list = []
    highest = 0
    lowest = 0
    humidity = 0

    highest_temp_date = None
    lowest_temp_date = None
    humidity_temp_date = None

    def __init__(self, data_lst):
        self.data = data_lst

    # creates a dictionary with key=date and value = Max temperature
    def set_max_list(self):
        self.max_list = {x['PKT']: int(x['Max TemperatureC']) for x in
                         self.data if x['Max TemperatureC'] not in (None, '')}

    # creates a dictionary with key=date and value = Min temperature
    def set_min_list(self):
        self.min_list = {x['PKT']: int(x['Min TemperatureC']) for x in
                         self.data if x['Min TemperatureC'] not in (None, '')}


class MonthlyReport(WeatherReport):
    def __init__(self, data_lst):
        WeatherReport.__init__(self, data_lst)

    # calculating averages of highest temp, lowest temp and mean humidity
    def calculate_statistics(self):
        self.set_max_list()
        self.set_min_list()
        self.highest = sum([i for i in self.max_list.values()])/len(
                            self.max_list)
        self.lowest = sum([i for i in self.min_list.values()])/len(
                            self.min_list)
        mean_hum_list = [int(x[' Mean Humidity']) for x in self.data
                         if x[' Mean Humidity'] not in (None, '')]
        self.humidity = sum(i for i in mean_hum_list)/len(mean_hum_list)

    def display_report(self):
        print("Monthly Report:")
        print("Highest Average: {0}{1}".format(self.highest, "C"))
        print("Lowest Average: {0}{1}".format(self.lowest, "C"))
        print("Average Mean Humidity: {0}{1}".format(self.humidity, "%"))


# for returning string of format: "MONTH_NAME DAY" for report displaying
def month_day(temp_date):
    month = calendar.month_name[datetime.strptime(temp_date, '%Y-%m-%d').month]
    day = str(datetime.strptime(temp_date, '%Y-%m-%d').day)
    return month+" " + day


class YearlyReport(WeatherReport):
    def __init__(self, data_lst):
        WeatherReport.__init__(self, data_lst)

    # calculating the highest temp, lowest temp and highest humidity of the
    # year along with their respective dates
    def calculate_statistics(self):
        self.set_max_list()
        self.set_min_list()

        self.highest_temp_date = max(self.max_list, key=self.max_list.get)
        self.highest = self.max_list[self.highest_temp_date]

        self.lowest_temp_date = min(self.min_list, key=self.min_list.get)
        self.lowest = self.min_list[self.lowest_temp_date]

        max_hum_list = {x['PKT']: int(x['Max Humidity']) for x in self.data
                        if x['Max Humidity'] not in (None, '')}
        self.humidity_temp_date = max(max_hum_list, key=max_hum_list.get)
        self.humidity = max_hum_list[self.humidity_temp_date]

    def display_report(self):
        print("Yearly Report:")
        print("Highest: {0}{1} on {2}".format(self.highest, 'C', month_day(
            self.highest_temp_date)))
        print("Lowest: {0}{1} on {2}".format(self.lowest, 'C', month_day(
            self.lowest_temp_date)))
        print("Humidity: {0}{1} on {2}".format(self.humidity, 'C', month_day(
            self.humidity_temp_date)))


class MonthlyBarChartReport(WeatherReport):
    def __init__(self, data_lst):
        WeatherReport.__init__(self, data_lst)

    def calculate_statistics(self):
        # creating dict with key=date, values=Max temperature, Min temperature
        self.data = {datetime.strptime(x['PKT'], '%Y-%m-%d').day:
                     (int(x['Max TemperatureC']),
                     int(x['Min TemperatureC'])) for x in self.data
                     if x['Max TemperatureC'] not in (None, '')}

    def display_report(self):
        print("Monthly Two line Bar chart Report:")
        for day, temp in self.data.items():
            print(day, end='')
            for i in range(0, temp[0]):
                print(colored('+', 'red'), end='')
            print("{0}{1}{2}{day_}".format(temp[0], 'C', '\n', day_=day),
                  end='')
            for i in range(0, temp[1]):
                print(colored('+', 'blue'), end='')
            print("{0}{1}".format(temp[1], 'C'))


class SingleLineMonthlyReport(MonthlyBarChartReport):
    def __init__(self, data_lst):
        MonthlyBarChartReport.__init__(self, data_lst)

    def display_report(self):
        print("Monthly Single Line  Bar chart Report:")
        for day, temp in self.data.items():
            print(day, end='')
            for i in range(0, temp[1]):
                print(colored('+', 'blue'), end='')
            for i in range(0, temp[0]):
                print(colored('+', 'red'), end='')
            print("{0}{1}-{2}{1}".format(temp[1], "C", temp[0]))


def fetch_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("FilePath", help="Path to file directory", type=str)
    parser.add_argument('-e', help='Yearly Weather Report', type=lambda d:
                        datetime.strptime(d, '%Y').strftime('%Y'))
    parser.add_argument('-a', help='Monthly Weather Report',
                        type=lambda d: datetime.strptime(d, '%Y/%m'))
    parser.add_argument('-c', help='Monthly Weather Report display Bar Chart',
                        type=lambda d: datetime.strptime(d, '%Y/%m'))
    parser.add_argument('-s', help='Single Line Monthly Weather Report display'
                                   ' Bar Chart',
                        type=lambda d: datetime.strptime(d, '%Y/%m'))

    arguments = parser.parse_args()
    return arguments


def iterate_directory():
    data = []
    for each in os.listdir(args.FilePath):
        with open(os.path.join(args.FilePath, each)) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(row)
    return data  # contains a list of dictionaries built from all the files


# concat string in format:"YEAR_MONTH ABRV" for searching string in filename
def year_mon_concat(year_month):
    return "{year}-{month}".format(year=year_month.strftime('%Y'),
                                   month=int(year_month.strftime('%m')))


# criteria = commandline argument passed e.g. year
def build_report_data(criteria, data_list):
    data = []
    for row in data_list:
        if 'PKST' in row:  # for consistency
            row['PKT'] = row.pop('PKST')
        if criteria in row['PKT']:
            data.append(row)
    return data


def build_report(args_):
    reports_list = []
    data_list = iterate_directory()
    if args_.e is not None:
        data = build_report_data(args_.e, data_list)
        rep = YearlyReport(data)
        reports_list.append(rep)

    if args_.a is not None:
        year_month = year_mon_concat(args_.a)
        data = build_report_data(year_month, data_list)
        rep = MonthlyReport(data)
        reports_list.append(rep)

    if args_.c is not None:
        year_month = year_mon_concat(args_.c)
        data = build_report_data(year_month, data_list)
        rep = MonthlyBarChartReport(data)
        reports_list.append(rep)

    if args_.s is not None:
        year_month = year_mon_concat(args_.s)
        data = build_report_data(year_month, data_list)
        rep = SingleLineMonthlyReport(data)
        reports_list.append(rep)

    for obj in reports_list:
        obj.calculate_statistics()
        obj.display_report()
        print('\n')

if __name__ == '__main__':
    args = fetch_arguments()
    build_report(args)
