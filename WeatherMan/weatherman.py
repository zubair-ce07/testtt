import os
# import sys
import argparse
import glob
import csv
import pprint
from collections import defaultdict


class FileParser:
    """This Class Read all files and make a nested dictionary of every day"""
    def __init__(self, directory):
        self.directory = directory
        self.weather_record = []

    def file_reader(self):
        """This function will read data from file and make a list"""
        for name in glob.glob(self.directory+"/*.txt"):
            with open(name, 'r') as file:
                next(file)
                reader = csv.DictReader(file)
                for row in reader:
                    if 'PKST' in row.keys():
                        date = row['PKST']
                    else:
                        date = row['PKT']
                    date = date.split('-')
                    if not date[0] == "<!":
                        choose_data = {'Max TemperatureC': row[
                            'Max TemperatureC'],
                            'Min TemperatureC': row[
                            'Min TemperatureC'],
                            'Max Humidity': row['Max Humidity'],
                            'Min Humidity': row[' Min Humidity']}
                        self.weather_record.append(
                            {date[0]: {
                                date[1]: {
                                    date[2]: choose_data
                                }}})
                    else:
                        continue

        return self.weather_record


class DataCalculation:
    """Data Calculation Class

    This class will calculate all type of max/min of temperature/humidity"""

    def __init__(self, data):
        self.data = data
        self.max_temperature = None
        self.min_temperatue = None
        self.max_humidity = None
        self.min_humidity = None
        self.max_temperature_variable = 0
        self.annual_data = dict()

    def calculate(self, reporttype):
        """This module will call the calculate function according reporttype"""
        available_data_of_years = set([elem2 for elem in self.data
                                       for elem2 in elem])
        if reporttype == 1:
            self.calculate_yearly(available_data_of_years)
        elif reporttype == 2:
            self.calculate_hotest_day_of_year(available_data_of_years)

        return self.annual_data

    def calculate_yearly(self, available_data_of_years):
        """This module will calculate annual max/min of temperature/humidity"""
        self.max_temperature = set()
        self.min_temperatue = set()
        self.max_humidity = set()
        self.min_humidity = set()
        for year in available_data_of_years:
            self.max_humidity.clear()
            self.min_temperatue.clear()
            self.max_temperature.clear()
            self.min_humidity.clear()
            for item in self.data:
                yearly_data = item.get(year)
                if yearly_data:
                    for month in yearly_data:
                        monthly_data = yearly_data.get(month)
                        for day in monthly_data:
                            day_data = monthly_data.get(day)
                            if day_data['Max TemperatureC']:
                                self.max_temperature.add(
                                    int(day_data['Max TemperatureC']))
                            if day_data['Min TemperatureC']:
                                self.min_temperatue.add(
                                    int(day_data['Min TemperatureC']))
                            if day_data['Max Humidity']:
                                self.max_humidity.add(
                                    int(day_data['Max Humidity']))
                            if day_data['Min Humidity']:
                                self.min_humidity.add(
                                    int(day_data['Min Humidity']))

            yearly_calculated_data = {
                'Max TemperatureC': max(self.max_temperature),
                'Min TemperatureC': min(self.min_temperatue),
                'Max Humidity': max(self.max_humidity),
                'Min Humidity': min(self.min_humidity)}
            self.annual_data[year] = yearly_calculated_data

    def calculate_hotest_day_of_year(self, available_data_of_years):
        """This module will calculate Hotest Day of each year"""
        for year in available_data_of_years:
            self.max_temperature_variable = 0
            for item in self.data:
                yearly_data = item.get(year)
                if yearly_data:
                    for month in yearly_data:
                        monthly_data = yearly_data.get(month)
                        for day in monthly_data:
                            day_data = monthly_data.get(day)
                            if day_data['Max TemperatureC']:
                                max_temp = int(day_data['Max TemperatureC'])
                                if max_temp > self.max_temperature_variable:
                                    self.day = day
                                    self.month = month
                                    self.year = year
                                    self.max_temperature_variable = max_temp
            hotest_day_of_year = {'Max TemperatureC':
                                  self.max_temperature_variable,
                                  'Day': self.day, 'Month': self.month}
            self.annual_data[year] = hotest_day_of_year


class PrintReport:
    """This class will print report according to reporttype"""

    def __init__(self, data):
        self.data = data

    def print_report(self, reporttype):
        if reporttype == 1:
            self.print_annualy()
        elif reporttype == 2:
            self.print_hotest_day_of_year()

    def print_annualy(self):
        print("Year    MaxTemp    MinTemp    MaxHumidity    MinHumidity")
        print("--------------------------------------------------------")
        for year in self.data:
            print(year, "    ", self.data[year]["Max TemperatureC"], "       ",
                  self.data[year]["Min TemperatureC"], "       ",
                  self.data[year]["Max Humidity"], "            ",
                  self.data[year]["Min Humidity"])

    def print_hotest_day_of_year(self):
        print("Year    Date             Temp")
        print("-----------------------------")
        for year in self.data:
            print(year, "    ", self.data[year]["Day"], "/",
                  self.data[year]["Month"], "/",
                  year, "    ",
                  self.data[year]["Max TemperatureC"])


def check_and_parse_system_arguments():
    """This Function checks for command line arguments and parse it"""
    arg = argparse.ArgumentParser()
    arg.add_argument("-r", "--report", required=True,
                     help="Report Number You Want")
    arg.add_argument("-d", "--directory", required=True,
                     help="Directory in which data is placed")
    arg_values = vars(arg.parse_args())
    return int(arg_values["report"]), arg_values["directory"]


def check_for_valid_argument(report, directory):
    """This function will be called after parsing of system arguments

    this function will check whether the argument recived is valid or not"""
    if report == 1 or report == 2:
        if not os.path.isdir(directory):
            print("Please Enter Valid Path of Directory")
            return False
        else:
            return True
    else:
        print("Please Enter Valid Report Number")
        print("1. For Annual Max/Min Temperature")
        print("2. For Hottest day of each year")
        return False


if __name__ == "__main__":
    reporttype, directory = check_and_parse_system_arguments()
    if not check_for_valid_argument(reporttype, directory):
        exit(0)

    parser = FileParser(directory)
    data = parser.file_reader()

    calculate = DataCalculation(data)
    annual_data = calculate.calculate(reporttype)

    printer = PrintReport(annual_data)
    printer.print_report(reporttype)
