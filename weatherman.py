import csv
import glob
import datetime
import argparse


class ReadFiles:
    def read_files(self, path):
        all_data = []
        for weather_file in glob.glob(f'{path}{"/"}{"*.txt"}'):
            for record in csv.DictReader(open(weather_file)):
                if self.is_valid_record(record):
                    all_data.append(WeatherRecord(record))

        return all_data

    def is_valid_record(self, record):

        if (record.get("PKT") or record.get("PKST")) and record.get("Max TemperatureC") and \
                record.get("Min TemperatureC") and record.get("Max Humidity") and record.get(" Mean Humidity") \
                and record.get("Mean TemperatureC") and record.get(" Min Humidity"):
            return True


class WeatherRecord:
    def __init__(self, record):
        date = record.get("PKT") or record.get("PKST")
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        self.max_temp = int(record.get("Max TemperatureC"))
        self.min_temp = int(record.get("Min TemperatureC"))
        self.max_humidity = int(record.get("Max Humidity"))
        self.mean_humidity = int(record.get(" Mean Humidity"))
        self.mean_temp = int(record.get("Mean TemperatureC"))
        self.min_humidity = int(record.get(" Min Humidity"))


class Calculator:
    def get_avg_temp(self, all_data, input_date):
        records = [record for record in all_data if record.date.year == input_date.year and \
                   record.date.month == input_date.month]

        avg_max_temp = sum([item.max_temp for item in records]) // len(records)
        avg_min_temp = sum([item.min_temp for item in records]) // len(records)
        avg_mean_humidity = sum([item.max_humidity for item in records]) // len(records)

        return avg_max_temp, avg_min_temp, avg_mean_humidity

    def get_temperatures(self, all_data, input_date):
        records = [record for record in all_data if record.date.year == input_date.year]

        max_temp = max(records, key=lambda item: item.max_temp)
        min_temp = max(records, key=lambda item: item.min_temp)
        max_humidity = max(records, key=lambda item: item.max_humidity)

        return max_temp, min_temp, max_humidity

    def get_graph_records(self, all_data, input_date):
        records = [record for record in all_data if record.date.year == input_date.year \
                   and record.date.month == input_date.month]

        return records


class ReportGenerator:
    BLUE = '\033[94m'
    RED = '\033[91m'

    def generate_avgs(self, avg_max_temp, avg_min_temp, avg_mean_humidity, input_date):
        print(f'{input_date: %B} {input_date.year}')
        print(f'Highest Average: {avg_max_temp}C')
        print(f'Lowest Average: {avg_min_temp}C')
        print(f'Average Mean Humidity: {avg_mean_humidity}%')

    def generate_req_temp(self, max_temp, min_temp, max_humidity):
        print(f'Highest: {max_temp.max_temp}C on{max_temp.date: %B} {max_temp.date: %d}')
        print(f'Lowest: {min_temp.min_temp}C on{min_temp.date: %B} {min_temp.date: %d}')
        print(f'Humidity: {max_humidity.max_humidity}% on {max_humidity.date: %B} {max_humidity.date: %d}')

    def generate_graph(self, records, input_date):
        print(f' {input_date : %B}{input_date : %Y}')

        for item in records:
             print(self.BLUE + str(item.date.day) + item.max_temp* '+' + str(item.max_temp))
             print(self.RED + str(item.date.day) + item.min_temp * '+' + str(item.min_temp))


def main():
    reader = ReadFiles()
    calculator = Calculator()
    generator = ReportGenerator()

    parser = argparse.ArgumentParser()
    parser.add_argument("year_temp", type=lambda year: datetime.datetime.strptime(year, '%Y').date())
    parser.add_argument("avg_month_temp", type=lambda month: datetime.datetime.strptime(month, '%Y/%m').date())
    parser.add_argument("graph_temp", type=lambda graph: datetime.datetime.strptime(graph, '%Y/%m').date())
    parser.add_argument("path")
    args = parser.parse_args()

    if args.path:
        data = reader.read_files(args.path)

    if args.year_temp:
        max_temp, min_temp, max_humidity = calculator.get_temperatures(data, args.year_temp)

    generator.generate_req_temp(max_temp, min_temp, max_humidity)

    if args.avg_month_temp:
        avg_max_temp, avg_min_temp, avg_mean_humidity = calculator.get_avg_temp(data, args.avg_month_temp)

    generator.generate_avgs(avg_max_temp, avg_min_temp, avg_mean_humidity, args.avg_month_temp)

    if args.graph_temp:
        records = calculator.get_graph_records(data, args.graph_temp)

    generator.generate_graph(records, args.graph_temp)


if __name__ == '__main__':
    main()
