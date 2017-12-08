import os
import re
import csv

from Classes import WeatherReading


def get_file_names( directory_path, args):

    directory_files = os.listdir(directory_path)
    regex = str(args.get('year')) + "_" +str(args.get('month'))

    if not args.get('month'):
        required_files = [os.path.join(directory_path, file_name) for file_name in directory_files if re.findall(args.get('year'), file_name)]
    else:
        required_files = [os.path.join(directory_path, file_name) for file_name in directory_files if re.findall(regex, file_name)]

    return read_files(required_files)


def read_files(files_to_read):

    file_rows = []

    for files in files_to_read:
        input_file = csv.DictReader(open(files))

        for row in input_file:
            weather = WeatherReading(row)
            file_rows.append(weather)

    return file_rows