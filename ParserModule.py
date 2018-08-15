"""This Module Parses All of the data coming from files"""

import os
from datetime import datetime

from WeatherRecordStructure import WeatherRecord

# List of months used while conversions
_total_months = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
    'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
    'Nov': 11, 'Dec': 12
}


def parser(directory_path, time_span):
    """This is the main function of this module, it takes directory and date to work on and in return
    it gives a list of records from the directory related to the specified dates"""
    try:
        work_directory = os.walk(directory_path)
    except FileNotFoundError:
        raise FileNotFoundError

    # Getting list of all files from the given directory
    try:
        record_files = list(work_directory)[0][2:][0]
    except IndexError:
        raise IndexError

    # Contain records of all the required directories
    required_records = []

    # Parsing the given time format
    year_required, month_required, day_required = time_parser(time_span)

    # It will iterate through all files and gives list of required files
    for record_file in record_files:
        if _is_file_required(record_file, year_required, month_required):
            required_records.append(record_file)

    # If records found
    if len(required_records) > 0:
        return _data_populator(directory_path, required_records, day_required)

    else:
        return None


def _data_populator(directory_path, records, day_given=None):
    """It takes path of directory with names of files as arguments
     and returns Structured Data in the form of list"""

    weather_structure = []
    for record in records:
        weather_structure.extend(_file_reader(directory_path, record, day_given))

    return weather_structure


def _file_reader(directory_path, file_name, specific_date=None):
    """It takes path of directory with names of files as arguments
     and returns Structured Data in the form of WeatherRecord Object list"""

    file_records = []
    month_file = open(directory_path + file_name, 'r')

    # First line contains information of file structure, so skipping them
    month_file.__next__()

    if not specific_date:
        lines = month_file.readlines()

        for line in lines:
            line.replace('\n', '')
            fields = line.split(',')

            date_pkt = datetime.strptime(fields[0], '%Y-%m-%d').date(),
            max_temperature_c = fields[1],
            mean_temperature_c = fields[2],
            min_temperature = fields[3],
            max_humidity = fields[7],
            mean_humidity = fields[8],
            min_humidity = fields[9],

            file_records.append(WeatherRecord(
                date_pkt,
                max_temperature_c,
                mean_temperature_c,
                min_temperature,
                max_humidity,
                mean_humidity,
                min_humidity,

            ))
    else:
        lines = month_file.readlines()
        lines = lines[int(specific_date) - 1]
        lines.replace('\n', '')
        fields = lines.split(',')

        date_pkt = datetime.strptime(fields[0], '%Y-%m-%d').date(),
        max_temperature_c = fields[1],
        mean_temperature_c = fields[2],
        min_temperature = fields[3],
        max_humidity = fields[7],
        mean_humidity = fields[8],
        min_humidity = fields[9],

        file_records.append(WeatherRecord(
            date_pkt,
            max_temperature_c,
            mean_temperature_c,
            min_temperature,
            max_humidity,
            mean_humidity,
            min_humidity,
        ))

    month_file.close()

    return file_records


def _is_file_required(name_file, year_required, month_required):
    """This function takes 'file name, month and year' as arguments to
     checks which files are required from the directory to be Parsed"""

    splitted_name = name_file.replace('.txt', '').split('_')
    year, month = splitted_name[2], splitted_name[3]

    if year_required and year_required == int(year):
        if month_required and month_required != _total_months[month]:
            return False
    else:
        return False

    return True


def time_parser(time_to_be_parsed):
    """It takes date in YYYY/MM/DD foramt and Returns the Accurate information
     of date by splitting it in Year, Month and Day"""

    # User can give year, month and day separated by '/', so here we split them
    bulk_date = time_to_be_parsed.split('/')
    try:
        if len(bulk_date) == 3:
            year_required, month_required, day_required = int(bulk_date[0]), int(bulk_date[1]), int(bulk_date[2])
        elif len(bulk_date) == 2:
            year_required, month_required, day_required = int(bulk_date[0]), int(bulk_date[1]), None
        elif len(bulk_date) == 1:
            year_required, month_required, day_required = int(bulk_date[0]), None, None
        else:
            year_required, month_required, day_required = None, None, None

        return year_required, month_required, day_required
    except TypeError:
        raise TypeError
