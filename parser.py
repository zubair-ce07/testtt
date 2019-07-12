from csv import DictReader
from datetime import datetime
from glob import glob
from weather_reading import WeatherReading
from reporter import Reports
import argparse
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
                complete_rec += [WeatherReading(record) for record in record_reader if
                                     self.validity_check(self, record)]
        return complete_rec


def argument_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='Local File Path on Your Machine')
    parser.add_argument('-e', '-yearly', type=lambda arg: datetime.strptime(arg, '%Y'), nargs="*")
    parser.add_argument('-a', '-monthly', type=lambda arg: datetime.strptime(arg, '%Y/%m'), nargs="*")
    parser.add_argument('-b', '-bonus', type=lambda arg: datetime.strptime(arg, '%Y/%m'), nargs="*")
    parser.add_argument('-c', '-chart', type=lambda arg: datetime.strptime(arg, '%Y/%m'), nargs="*")
    return parser.parse_args()

if __name__ == "__main__":
    calculator = Calculations()
    generate_rep = Reports()
    args = argument_parse()
    files_path = args.file_path
    weather_records = Parser.readfile(Parser, files_path)

    if args.e:
            for arguments in args.e:
                montly_results = calculator.calculations_yearly(weather_records, arguments.date().year)
                generate_rep.report_yearly(montly_results)

    if args.a:
            for arguments in args.a:
                montly_results = calculator.calculations_montly(weather_records, arguments.date())
                generate_rep.report_monthly(montly_results)

    if args.b:
            for arguments in args.b:
                records = calculator.record_month(weather_records, arguments.date())
                generate_rep.report_chart(records, True)

    if args.c:
            for arguments in args.c:
                records = calculator.record_month(weather_records, arguments.date())
                generate_rep.report_chart(records)

