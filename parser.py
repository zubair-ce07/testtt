from csv import DictReader
from datetime import datetime
from glob import glob
from weather_data import WeatherData
from reporter import ReportGenerator
import argparse
import os
import re
from calculations import Calculations

class Parser:

    def validity_check(self, record):
        valid_record = [record["Max TemperatureC"],
                        record["Min TemperatureC"],
                        record[" Mean Humidity"],
                        record.get("PKT",
                        record.get("PKST"))
                        ]
        if all(valid_record):
            return True

    def readfile(self, files_path):
        complete_rec = []
        files_path += "Murree_weather_*"
        for files in glob(files_path):

            with open(files, "r") as single_file:
                record_reader = DictReader(single_file)
                complete_rec += [WeatherData(record) for record in record_reader if
                                     self.validity_check(self, record)]
        return complete_rec

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='Local File Path on Your Machine')
    parser.add_argument('-e', '-yearly', type=lambda arg: datetime.strptime(arg, '%Y'), nargs="*")
    parser.add_argument('-a', '-monthly', type=lambda arg: datetime.strptime(arg, '%Y/%m'), nargs="*")
    return parser.parse_args()


if __name__ == "__main__":
    calculator = Calculations()
    generate_rep = ReportGenerator()
    input_arguments = arg_parser()
    files_path = input_arguments.file_path
    weather_records = Parser.readfile(Parser, files_path)


    if input_arguments.e:
        for arguments in input_arguments.e:
            results = calculator.report_yearly(weather_records, arguments.date().year)
            generate_rep.yearly(results)

    if input_arguments.a:
        for arguments in input_arguments.a:
            results = calculator.report_monthly(weather_records, arguments.date())
            generate_rep.monthly(results)
