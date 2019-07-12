from csv import DictReader
from glob import glob
from weather_reading import WeatherReading
from reporter import Reports
from calculations import Calculations
from Arguments import argument_parse


class FileParser:


    def validity_check(self, record):
        valid_record = [record["Max TemperatureC"],
                        record["Min TemperatureC"],
                        record[" Mean Humidity"],
                        record.get("PKT")
                        ]
        if all(valid_record):
            return True

    def extract_data(self, path):
        complete_rec = []
        path += f"Murree_weather_*"
        for files in glob(path):

            with open(files, "r") as single_file:
                record_reader = DictReader(single_file)
                complete_rec += [WeatherReading(record) for record in record_reader if
                                     self.validity_check(self, record)]
        return complete_rec


if __name__ == "__main__":
    calculator = Calculations()
    generate_rep = Reports()
    args = argument_parse()
    path = args.file_path
    total_records = FileParser.extract_data(FileParser, path)

    if args.e:
            for arguments in args.e:
                montly_results = calculator.calculations_yearly(total_records, arguments.date().year)
                generate_rep.report_yearly(montly_results)

    if args.a:
            for arguments in args.a:
                montly_results = calculator.calculations_montly(total_records, arguments.date())
                generate_rep.report_monthly(montly_results)

    if args.b:
            for arguments in args.b:
                records = calculator.record_month(total_records, arguments.date())
                generate_rep.single_chart(records)

    if args.c:
            for arguments in args.c:
                records = calculator.record_month(total_records, arguments.date())
                generate_rep.double_chart(records)

