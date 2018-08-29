""" Contain all common functions """
from datetime import datetime
import csv
from classes import (Temperature, Humidity, DayRecord)
from constants import DEFAULT


csv.register_dialect('dialect', delimiter=',', skipinitialspace=True)


def get_path_file(path_to_dir, year, month):
    """Return path to the required file given the year and month"""
    file_path = "{}/Murree_weather_{}_{}.txt".format(path_to_dir,
                                                     year,
                                                     month)
    return file_path


def read_single_line_record(day_data):
    """ get single line record and return class object"""
    try:
        temp = Temperature(int(day_data["Max TemperatureC"] or DEFAULT),
                           int(day_data["Mean TemperatureC"] or DEFAULT),
                           int(day_data["Min TemperatureC"] or 1000))

        humidity = Humidity(int(day_data["Max Humidity"] or DEFAULT),
                            int(day_data[" Min Humidity"] or 1000),
                            int(day_data[" Mean Humidity"] or DEFAULT))
        date = datetime.strptime(day_data["PKT"], '%Y-%m-%d')
        day_record = DayRecord(date, temp, humidity)
        return day_record
    except:
        return None


def get_month_data_in_year_list(file_name, rec_list, print_except):
    """ get year list and append month data of given filename """
    try:
        with open(file_name, mode='r') as reader:
            csv_reader = csv.DictReader(reader)
            for row in csv_reader:
                day_record = read_single_line_record(row)
                rec_list.append(day_record)

    except IOError as err:
        if print_except is True:
            print("I/O error({0}: {1})".format(err.errno, err.strerror))
        print("", end="")
