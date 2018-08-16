import os
import argparse
from glob import glob
import csv
from datetime import datetime


class FileParser:
    """This Class Read all files and make a nested dictionary of every day"""

    def __init__(self, directory):
        self.directory = directory
        self.weather_record = {}

    def file_reader(self):
        """This function will read data from file and make a list"""

        if not len(glob(os.path.join(
            self.directory,
            'lahore_weather_[0-9]*_[A-Z][a-z]*.txt'
        ))) == 0:
            for report_path in glob(os.path.join(
                    self.directory,
                    'lahore_weather_[0-9]*_[A-Z][a-z]*.txt'
            )):
                with open(report_path, 'r') as report_file:
                    next(report_file)
                    reader = csv.DictReader(report_file)
                    for row in reader:
                        if 'PKST' in row.keys():
                            if '<!' not in row['PKST']:
                                date = datetime.strptime(
                                    row['PKST'],
                                    "%Y-%m-%d"
                                    )
                            else:
                                continue
                        else:
                            if '<!' not in row['PKT']:
                                date = datetime.strptime(
                                    row['PKT'],
                                    "%Y-%m-%d"
                                    )
                            else:
                                continue
                        choose_data = {
                            'Max TemperatureC': row['Max TemperatureC'],
                            'Min TemperatureC': row['Min TemperatureC'],
                            'Max Humidity': row['Max Humidity'],
                            'Min Humidity': row[' Min Humidity']
                        }
                        self.weather_record[date] = choose_data
        else:
            print("This Directory doesn't contain any weather report")
            exit(0)
        return self.weather_record


class WeatherReport:
    """
    Weather Report Class
    This class will calculate all type of max/min of temperature/humidity
    This class will also print the reports
    """

    def __init__(self, data):
        self.data = data
        self.annual_data = {}

    def calculate(self, reporttype):
        """This module will call the calculate function according reporttype"""
        available_data_of_years = set([elem.year for elem in self.data])
        if reporttype == 1:
            self.get_yearly_weather_report(available_data_of_years)
            self.print_annualy()
        elif reporttype == 2:
            self.get_hotest_day_of_year(available_data_of_years)
            self.print_hotest_day_of_year()

        return self.annual_data

    def get_yearly_weather_report(self, available_data_of_years):
        """This module will calculate annual max/min of temperature/humidity"""
        for year in available_data_of_years:
            self.max_annual_temperature = set()
            self.min_annual_temperatue = set()
            self.max_annual_humidity = set()
            self.min_humidity = set()
            for item in self.data:
                if item.year == year:
                    if self.data[item]['Max TemperatureC']:
                        self.max_annual_temperature.add(
                            int(self.data[item]['Max TemperatureC'])
                        )
                    if self.data[item]['Min TemperatureC']:
                        self.min_annual_temperatue.add(
                            int(self.data[item]['Min TemperatureC'])
                        )
                    if self.data[item]['Max Humidity']:
                        self.max_annual_humidity.add(
                            int(self.data[item]['Max Humidity'])
                        )
                    if self.data[item]['Min Humidity']:
                        self.min_humidity.add(
                            int(self.data[item]['Min Humidity'])
                        )

            yearly_calculated_data = {
                'Max TemperatureC': max(self.max_annual_temperature),
                'Min TemperatureC': min(self.min_annual_temperatue),
                'Max Humidity': max(self.max_annual_humidity),
                'Min Humidity': min(self.min_humidity)
            }
            self.annual_data[year] = yearly_calculated_data

    def get_hotest_day_of_year(self, available_data_of_years):
        """This module will calculate Hotest Day of each year"""
        for year in available_data_of_years:
            self.monthly_max_temperature = 0
            for item in self.data:
                if item.year == year:
                    if self.data[item]['Max TemperatureC']:
                        max_temp = int(self.data[item]['Max TemperatureC'])
                        if max_temp > self.monthly_max_temperature:
                            self.day = item.day
                            self.month = item.month
                            self.year = item.year
                            self.monthly_max_temperature = max_temp

            hotest_day_of_year = {
                'Max TemperatureC': self.monthly_max_temperature,
                'Day': self.day,
                'Month': self.month
            }

            self.annual_data[year] = hotest_day_of_year

    def print_annualy(self):
        """This Module will print annual report"""
        print("Year    MaxTemp    MinTemp    MaxHumidity    MinHumidity")
        print("--------------------------------------------------------")
        for year in self.annual_data:
            print(
                year, "    ", self.annual_data[year]["Max TemperatureC"],
                "       ",
                self.annual_data[year]["Min TemperatureC"],
                "       ",
                self.annual_data[year]["Max Humidity"],
                "            ",
                self.annual_data[year]["Min Humidity"]
            )

    def print_hotest_day_of_year(self):
        """This module will print hotest day of each year"""
        print("Year    Date             Temp")
        print("-----------------------------")
        for year in self.annual_data:
            print(year, "    ", self.annual_data[year]["Day"], "/",
                  self.annual_data[year]["Month"], "/",
                  year, "    ",
                  self.annual_data[year]["Max TemperatureC"])


def parse_arguments():
    """This Function checks for command line arguments and parse it"""
    arg = argparse.ArgumentParser()
    arg.add_argument("-r", "--report", required=True,
                     help="Report Number You Want")
    arg.add_argument("-d", "--directory", required=True,
                     help="Directory in which data is placed")
    arg_values = vars(arg.parse_args())
    return int(arg_values["report"]), arg_values["directory"]


def validate_arguments(report, directory):
    """This function will be called after parsing of system arguments

    this function will check whether the argument recived is valid or not"""
    if report in [1, 2]:
        if not os.path.isdir(directory):
            print("Please Enter Valid Path of Directory")
            return False
        if not os.listdir(directory):
            print("Directory is Empty! Please Enter Valid Path")
            return False
        return True
    else:
        print("Please Enter Valid Report Number")
        print("1. For Annual Max/Min Temperature")
        print("2. For Hottest day of each year")
        return False


def generate_and_print_report():
    """This function will generate and print the report"""
    reporttype, directory = parse_arguments()
    if validate_arguments(reporttype, directory):
        parser = FileParser(directory)
        data = parser.file_reader()

        calculate = WeatherReport(data)
        annual_data = calculate.calculate(reporttype)


if __name__ == "__main__":
    generate_and_print_report()
