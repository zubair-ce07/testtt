""" Contain all common functions """
from datetime import datetime
import csv
from classes import Temperature, Humidity, DayRecord


def get_path_file(path_to_dir, year, month):
    """Return path to the required file given the year and month"""
    month = month.capitalize()
    file_path = f"{path_to_dir}/Murree_weather_{year}_{month}.txt"
    return file_path


def read_single_line_record(day_data):
    """ get single line record and return class object"""
    try:
        
        temperature = Temperature(int(day_data["Max TemperatureC"] or None),
                           int(day_data["Mean TemperatureC"] or None),
                           int(day_data["Min TemperatureC"]))

        humidity = Humidity(int(day_data["Max Humidity"] or None),
                            int(day_data[" Min Humidity"] or None),
                            int(day_data[" Mean Humidity"] or None))
        date = datetime.strptime(day_data["PKT"], '%Y-%m-%d')
        day_record = DayRecord(date, temperature, humidity)
        return day_record
    except:
        return None


def get_month_data_in_year_list(file_name, rec_list, print_except):
    """ get year list and append month data of given filename """
    try:
        with open(file_name, mode='r') as reader:
            csv_reader = csv.DictReader(reader, delimiter=',')
            for row in csv_reader:
                day_record = read_single_line_record(row)
                rec_list.append(day_record)

    except IOError as err:
        if print_except is True:
            print(f"I/O error({err.errno}: {err.strerror})")
        print("", end="")
