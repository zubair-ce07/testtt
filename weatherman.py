import getopt
import sys
import os
import csv
import calendar
from os import path


USAGE_STRING = r'usage: weatherman <files directory> -opt1 arg1 [-opt2 arg2 [-opt3 arg3]]' + (
               '\nopt1, opt2, opt3: a, e, c' + '\narg1, arg2, arg3: Date\n'
)
VALID_SWITCHES = ['-a', '-e', '-c']
NO_DATA_ERROR = 'No data found for given date'
MAX_TEMPRATURE = 'Max TemperatureC'
MIN_TEMPRATURE = 'Min TemperatureC'
MAX_HUMIDITY = 'Max Humidity'
MEAN_HUMIDITY = ' Mean Humidity'
DATE = 'PKT'
DATES = 'PKST'
RED = '\033[91m'
BLUE = '\033[34m'
END = '\033[0m'
PLUS = '+'


class WeatherReport:
    def __init__(self, data):
        self._weather_data = data


class ExtremeWeatherReport(WeatherReport):
    def __init__(self, data):
        super().__init__(data)
        self._highest_temp = -273
        self._lowest_temp = 200
        self._most_humid = 0
        self._highest_temp_date = -273
        self._lowest_temp_date = 200
        self._most_humid_date = 0

    def calculate(self):
        if len(self._weather_data):
            for row in self._weather_data:
                day_max_temp = row[MAX_TEMPRATURE]
                day_min_temp = row[MIN_TEMPRATURE]
                day_max_humid = row[MAX_HUMIDITY]

                if day_max_temp and float(day_max_temp) > self._highest_temp:
                    self._highest_temp = float(day_max_temp)
                    self._highest_temp_date = get_date_value(row)

                if day_min_temp and float(day_min_temp) < self._lowest_temp:
                    self._lowest_temp = float(day_min_temp)
                    self._lowest_temp_date = get_date_value(row)

                if day_max_humid and float(day_max_humid) > self._most_humid:
                    self._most_humid = float(day_max_humid)
                    self._most_humid_date = get_date_value(row)

    def print_report(self):
        if len(self._weather_data):
            month = calendar.month_name[int(self._highest_temp_date.split('-')[1])]
            day = self._highest_temp_date.split('-')[2]
            print('Highest: %.1fC on %s %s' % (self._highest_temp, month, day))

            month = calendar.month_name[int(self._lowest_temp_date.split('-')[1])]
            day = self._lowest_temp_date.split('-')[2]
            print('Lowest: %.1fC on %s %s' % (self._lowest_temp, month, day))

            month = calendar.month_name[int(self._most_humid_date.split('-')[1])]
            day = self._most_humid_date.split('-')[2]
            print('Humidity: %.1f%% on %s %s\n' % (self._most_humid, month, day))
        else:
            print(NO_DATA_ERROR)


class AverageWeatherReport(WeatherReport):
    def __init__(self, data):
        super().__init__(data)

        self._avg_highest = -273
        self._avg_lowest = 200
        self._avg_humid = 0

    def calculate(self):
        if len(self._weather_data):
            total_highest_temp = 0
            total_lowest_temp = 0
            total_mean_humid = 0

            for row in self._weather_data:
                if row[MAX_TEMPRATURE]:
                    total_highest_temp += float(row[MAX_TEMPRATURE])

                if row[MIN_TEMPRATURE]:
                    total_lowest_temp += float(row[MIN_TEMPRATURE])

                if row[MEAN_HUMIDITY]:
                    total_mean_humid += float(row[MEAN_HUMIDITY])

            self._avg_highest = float(total_highest_temp / len(self._weather_data))
            self._avg_lowest = float(total_lowest_temp / len(self._weather_data))
            self._avg_humid = float(total_mean_humid / len(self._weather_data))

    def print_report(self):
        if len(self._weather_data):
            print('Highest average: %.2fC' % self._avg_highest)
            print('Lowest average: %.2fC' % self._avg_lowest)
            print('Average Mean Humidity: %.2f%%\n' % self._avg_humid)
        else:
            print(NO_DATA_ERROR)


class ChartWeatherReport(WeatherReport):
    def __init__(self, data):
        super().__init__(data)
        self._chart = ''

    def calculate(self):
        if len(self._weather_data):
            for row in self._weather_data:
                min_temp = 0
                max_temp = 0
                str_list = []
                str_chart = ''
                date_of_month = get_date_value(row).split('-')[2].strip().zfill(2)
                str_list.append(date_of_month)

                if row[MIN_TEMPRATURE].strip():
                    min_temp = int(row[MIN_TEMPRATURE])
                    if min_temp > 0:
                        str_chart = str_chart + BLUE + PLUS*min_temp + END

                if row[MAX_TEMPRATURE].strip():
                    max_temp = int(row[MAX_TEMPRATURE])
                    if max_temp > 0:
                        str_chart = str_chart + RED + PLUS*max_temp + END

                str_list.append(str_chart)
                str_list.append('%iC - %iC\n' % (min_temp, max_temp))
                self._chart += ' '.join(str_list)

    def print_report(self):
        if len(self._weather_data):
            print(self._chart)
        else:
            print(NO_DATA_ERROR)


def exit_weatherman(message):
    """Prints the error message and exit"""
    print(message)
    sys.exit(2)


def directory_sanity_check(directory_path):
    """Checks if the given directory_path is valid one for data files"""
    # Check if path is directory, throw error otherwise
    if not path.isdir(directory_path):
        exit_weatherman('invalid file directory: %s' % dir_path)
    # If there are no child then then we don't have right directory of file, throw error
    if len(os.listdir(directory_path)) == 0:
        exit_weatherman('No files in directory')


def get_date_value(row):
    #Some data files have rather unusual tag for date. Catering both
    try:
        return row[DATE]
    except KeyError:
        return row[DATES]


def get_report_object(operation, data, month = 0):
    """Returns object on the basis of operation"""
    if operation == '-a':
        if month:
            return AverageWeatherReport(data)
        else:
            return 'Invalid month'
    elif operation == '-e':
        return ExtremeWeatherReport(data)
    elif operation == '-c':
        if month:
            return ChartWeatherReport(data)
        else:
            return 'Invalid month'


def extract_year_month(str_date):
    """Extract year and month from string"""
    int_year = 0
    int_month = 0
    if len(str_date) < 4:
        exit_weatherman('Invalid year')
    elif len(str_date) == 4 and str_date.isnumeric():
        int_year = int(str_date)
    elif len(str_date) > 5 and str_date.find(r'/', 4) > -1:
        int_year = int(str_date.split(r'/')[0])
        int_month = int(str_date.split(r'/')[1])
    else:
        exit_weatherman('Invalid date format')

    if int_month not in range(0, 13):
        exit_weatherman('invalid month')
    return int_year, int_month


def get_data_for_date(directory_path, year, month):
    """Prepare and returnd the data for given month and year"""
    return_data = []
    # Get files from the directory
    files = os.listdir(directory_path)
    month = calendar.month_abbr[month]
    for file_ in files:
        if file_.find(str(year)) < 0:
            continue
        if month and file_.find(month) < 0:
            continue
        relative_path = path.join(directory_path, file_)
        with open(relative_path) as csv_file:
            return_data.extend(csv.DictReader(csv_file))
    return return_data

if __name__ == '__main__':
    # We will needing minimum 4 arguments to make it work
    if len(sys.argv) < 4:
        exit_weatherman(USAGE_STRING)
    # Get path where data files are placed
    dir_path = sys.argv[1]
    # Check if directory is OK
    directory_sanity_check(dir_path)
    # Get command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[2:], 'ha:e:c:')
    except getopt.GetoptError as optionsError:
        print('Invalid options ', optionsError)
        exit_weatherman(USAGE_STRING)
    # Iterate over options
    for opt, arg in opts:
        if opt.strip() in VALID_SWITCHES:
            year_, month_ = extract_year_month(arg.strip())
            data_ = get_data_for_date(dir_path, year_, month_)
            report_object = get_report_object(opt.strip(), data_, month_)
            try:
                report_object.calculate()
                report_object.print_report()
            except AttributeError:
                exit_weatherman(report_object)
        else:
            exit_weatherman(USAGE_STRING)

