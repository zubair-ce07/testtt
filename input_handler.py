import argparse
import csv
import glob

from datetime import datetime

from weather_container import RecordHolder


class Parser:

    def __init__(self):
        self.file_directory = ''

    def initialization(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('file_path',
                            help='The file path of weather files')
        parser.add_argument('-e', '-yearly',
                            type=lambda arg: datetime.strptime(
                                arg, '%Y'), nargs="*")
        parser.add_argument('-a', '-monthly',
                            type=lambda arg: datetime.strptime(
                                arg, '%Y/%m'), nargs="*")
        parser.add_argument('-b', '-bonus',
                            type=lambda arg: datetime.strptime(
                                arg, '%Y/%m'), nargs="*")
        parsed_data = parser.parse_args()
        return parsed_data

    def record_validity(self, single_record):
        if single_record["Max TemperatureC"] == '' or \
                single_record["Min TemperatureC"] == '' or \
                single_record[" Mean Humidity"] == '':
            return False

    def data_extractor(self, directory_file):

        compiled_records = []
        file_path = directory_file + 'Murree_weather_' + '*'
        for files in glob.glob(file_path):
            with open(files, "r") as single_file:
                read_record = csv.DictReader(single_file)
                for records in read_record:

                    if self.record_validity(records,records) == False:
                        continue
                    else:
                        compiled_records.append((RecordHolder(records)))

        return compiled_records
