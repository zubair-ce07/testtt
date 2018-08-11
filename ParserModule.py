"""This Module Parses All of the data coming from files"""

import os
from datetime import datetime

from WeatherRecordStructure import WeatherRecord

# List of months used while conversions
_list_months = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
    'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
    'Nov': 11, 'Dec': 12
}


def parser_(path_dir=None, time_span=None):
    """This Function Parses The given Directory and Related Content"""
    try:
        object_dir = os.walk(path_dir)
    except FileNotFoundError:
        raise FileNotFoundError

    # Getting list of all files from the given directory
    list_record_files = list(object_dir)[0][2:][0]

    # Contain records of all the required directories
    list_required_records = []

    # Parsing the given time format
    year_required, month_required, day_required = time_parser(time_span)

    # It will iterate through all files and gives list of required files
    for record_file in list_record_files:
        if _is_required(record_file, year_required, month_required):
            list_required_records.append(record_file)

    # If records found
    if len(list_required_records) > 0:

        # Records which doesn't require date to be parsed
        if day_required is not None:
            list_records = _data_populator(path_dir, list_required_records, day_required)

        # Records which does require date to be parsed
        else:
            list_records = _data_populator(path_dir, list_required_records)

        return list_records

    else:
        return None


def _data_populator(path_dir, records, day_given=None):
    """It returns Structured Data in the form of list"""
    list_weather_structure = []

    if day_given is None:
        for record in records:
            list_weather_structure.extend(_file_reader(path_dir, record))
    else:
        for record in records:
            list_weather_structure.extend(_file_reader(path_dir, record, day_given))

    return list_weather_structure


def _file_reader(path_dir, file_name, specific_date=None):
    """This function Reads Data from Files and Store them"""
    list_file_records = []
    month_file = open(path_dir + file_name, 'r')

    # First line contains information of file structure, so skipping them
    month_file.__next__()

    if specific_date is None:
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

            list_file_records.append(WeatherRecord(
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

        list_file_records.append(WeatherRecord(
            date_pkt,
            max_temperature_c,
            mean_temperature_c,
            min_temperature,
            max_humidity,
            mean_humidity,
            min_humidity,
        ))

    month_file.close()

    return list_file_records


def _is_required(name_file, year_required, month_required):
    """This function checks which files are required in from the directory to be Parsed"""
    name_splited = name_file.replace('.txt', '').split('_')
    year_, month_ = name_splited[2], name_splited[3]

    try:
        if year_required is not None:
            if int(year_required) == int(year_):
                if month_required is not None:
                    month_ = _list_months[month_]
                    if int(month_required) == int(month_):
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False
        else:
            return False
    except:
        return False


def time_parser(time_to_be_parsed):
    """It Returns the Accurate information of date by splitting it in Year, Month and Date"""
    bulk_date = time_to_be_parsed.split('/')
    if len(bulk_date) == 3:
        year_required, month_required, day_required = bulk_date[0], bulk_date[1], bulk_date[2]
    elif len(bulk_date) == 2:
        year_required, month_required, day_required = bulk_date[0], bulk_date[1], None
    elif len(bulk_date) == 1:
        year_required, month_required, day_required = bulk_date[0], None, None
    else:
        year_required, month_required, day_required = None, None, None

    return year_required, month_required, day_required
