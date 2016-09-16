import csv
import argparse
import fnmatch
import os
from functools import reduce
import calendar


class Weather(object):
    def __init__(self, report_date, max_temp_c, mean_temp_c, min_temp_c, max_humidity, mean_humidity):
        parsed_date = report_date.split("-")
        self.day = int(parsed_date[2])
        self.month = int(parsed_date[1])
        self.year = int(parsed_date[0])
        self.max_temp_c = max_temp_c
        self.mean_temp_c = mean_temp_c
        self.min_temp_c = min_temp_c
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity

    @staticmethod
    def row_to_weather(row):
        report_date = row.get("PKT") or row.get("PKST")
        max_temp_c = int(row["Max TemperatureC"]) if row["Max TemperatureC"] else None
        max_humidity = int(row["Max Humidity"]) if row["Max Humidity"] else None
        min_temp_c = int(row["Min TemperatureC"]) if row["Min TemperatureC"] else None
        mean_temp_c = int(row["Mean TemperatureC"]) if row["Mean TemperatureC"] else None
        mean_humidity = int(row[" Mean Humidity"]) if row[" Mean Humidity"] else None
        return Weather(report_date, max_temp_c, mean_temp_c, min_temp_c, max_humidity, mean_humidity)

    @staticmethod
    def get_lowest(weather_records, column_name):
        condition = [record for record in weather_records if getattr(record, column_name) is not None]
        sorted_list = sorted(condition, key=lambda record: getattr(record, column_name), reverse=False)
        return sorted_list[0] if sorted_list else None

    @staticmethod
    def get_highest(weather_records, column_name):
        condition = [record for record in weather_records if getattr(record, column_name) is not None]
        sorted_list = sorted(condition, key=lambda record: getattr(record, column_name), reverse=True)
        return sorted_list[0] if sorted_list else None

    @staticmethod
    def get_average(weather_records, column_name):
        weather_records_filtered = [getattr(z, column_name) for z in weather_records if getattr(z, column_name) is not None]
        if len(weather_records_filtered) is 0:
            return 0
        return reduce(lambda x, y: x + y, weather_records_filtered)/len(weather_records_filtered)


class WeatherParser(object):
    def __init__(self, path, year, month=0):
        self.file_names = []
        self.path = path
        self.year = year
        self.month = month
        self.parse_file_names()

    def parse_file_names(self):
        if self.month:
            pattern = "*{}*{}.txt".format(self.year, calendar.month_abbr[self.month])
            for file in os.listdir(os.path.basename(self.path)):
                if fnmatch.fnmatch(file, pattern):
                    self.file_names.append(file)
        else:
            for file in os.listdir(os.path.basename(self.path)):
                if fnmatch.fnmatch(file, "*{}_*.txt".format(self.year)):
                    self.file_names.append(file)

    def get_rows(self):
        file_not_found_count = 0
        weather_records = []
        if len(self.file_names) is 0:
            raise FileNotFoundError
        for file_name in self.file_names:
            try:
                full_path = os.path.join(os.path.basename(self.path), file_name)
                csv_file = open(full_path, "r")
                next(csv_file)
                reader = csv.DictReader(csv_file, delimiter=',')
                for row in WeatherParser.get_next_row(reader):
                    weather_records.append(Weather.row_to_weather(row))
            except:
                file_not_found_count += 1
                if file_not_found_count is len(self.file_names):
                    raise
        return weather_records

    @staticmethod
    def get_next_row(reader):
        prev = None
        for row in reader:
            if prev:
                yield prev
            prev = row


class ReportGenerator(object):
    def __init__(self, path, year, month=0):
        weather_parser = WeatherParser(path, year, month)
        self.weather_records = weather_parser.get_rows()

    def generate_extreme_condition_report(self):
        current = Weather.get_highest(self.weather_records, 'max_temp_c')
        print("Highest: {}C on {} {}".format(current.max_temp_c, calendar.month_name[current.month], current.day))
        current = Weather.get_lowest(self.weather_records, 'min_temp_c')
        print("Lowest: {}C on {} {}".format(current.min_temp_c, calendar.month_name[current.month], current.day))
        current = Weather.get_highest(self.weather_records, "max_humidity")
        print("Humid: {}% on {} {}".format(current.max_humidity, calendar.month_name[current.month], current.day))

    def generate_average_condition_report(self):
        current = Weather.get_highest(self.weather_records, 'mean_temp_c')
        print("Highest Average: {}C".format(current.mean_temp_c))
        current = Weather.get_lowest(self.weather_records, 'mean_temp_c')
        print("Lowest Average:  {}C".format(current.mean_temp_c))
        current = Weather.get_average(self.weather_records, 'mean_humidity')
        print("Average Humidity:  {:.2f}%".format(current))

    def generate_multi_line_bar_chart(self):
        record = self.weather_records[0]
        print(calendar.month_name[record.month], record.year)
        for record in self.weather_records:
            if record.max_temp_c is None:
                continue
            print("{}\033[91m".format(record.day), "+"*record.max_temp_c, "\033[0m{}C".format(record.max_temp_c), sep="")
            print("{}\033[94m".format(record.day), "+"*record.min_temp_c, "\033[0m{}C".format(record.min_temp_c), sep="")

    def generate_single_line_bar_chart(self):
        record = self.weather_records[0]
        print(calendar.month_name[record.month], record.year)
        for record in self.weather_records:
            if record.max_temp_c is None or record.min_temp_c is None:
                continue
            print(record.day, "\033[94m+"*record.min_temp_c, "\033[91m+"*record.max_temp_c, sep="", end="")
            print("\033[0m{}C-{}C".format(record.min_temp_c, record.max_temp_c))


def main():
    parser = argparse.ArgumentParser(description='Weather Data Analyser')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', help='Averages', nargs=2)
    group.add_argument('-s', help='Single Line Charts', nargs=2)
    group.add_argument('-c', help='Charts', nargs=2)
    group.add_argument('-e', help='Extremes', nargs=2)
    parsed = parser.parse_args()
    try:
        if parsed.e:
            report_generator = ReportGenerator(parsed.e[1], parsed.e[0])
            report_generator.generate_extreme_condition_report()
        elif parsed.a:
            temp = parsed.a[0].split("/")
            report_generator = ReportGenerator(parsed.a[1], temp[0], int(temp[1]))
            report_generator.generate_average_condition_report()
        elif parsed.c:
            temp = parsed.c[0].split("/")
            report_generator = ReportGenerator(parsed.c[1], temp[0], int(temp[1]))
            report_generator.generate_multi_line_bar_chart()
        elif parsed.s:
            temp = parsed.s[0].split("/")
            report_generator = ReportGenerator(parsed.s[1], temp[0], int(temp[1]))
            report_generator.generate_single_line_bar_chart()
    except FileNotFoundError:
        print("No Such File Exists!!")
        exit(1)
    except Exception as e:
        print(e)
        print("usage: weatherman.py [-h] (-a year/month path | -s year/month path | -c year/month path "
              "| -e year path)\nweatherman.py: error correct argument is required")
        exit(1)

if __name__ == "__main__":
    main()
