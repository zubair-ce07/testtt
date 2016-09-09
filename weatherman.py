from datetime import datetime
import csv
import argparse
import fnmatch
import os


class Weather(object):
    __date_format = "%Y-%m-%d"

    def __init__(self, report_date, max_temp_c, mean_temp_c, min_temp_c, max_humidity, mean_humidity):
        self.report_date = report_date
        self.max_temp_c = max_temp_c
        self.mean_temp_c = mean_temp_c
        self.min_temp_c = min_temp_c
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity

    @staticmethod
    def row_to_weather(row):
        report_date = Util.get_formatted_date(row.get("PKT") or row.get("PKST"))
        try:
            max_temp_c = int(row.get("Max TemperatureC"))
        except:
            max_temp_c = None
        try:
            mean_temp_c = int(row.get("Mean TemperatureC"))
        except:
            mean_temp_c = None
        try:
            min_temp_c = int(row.get("Min TemperatureC"))
        except:
            min_temp_c = None
        try:
            max_humidity = int(row.get("Max Humidity"))
        except:
            max_humidity = None
        try:
            mean_humidity = int(row.get(" Mean Humidity"))
        except:
            mean_humidity = None
        return Weather(report_date, max_temp_c, mean_temp_c, min_temp_c, max_humidity, mean_humidity)

    @staticmethod
    def get_lowest(weather_records, column_name):
        condition = [record for record in weather_records if getattr(record, column_name) is not None]
        sorted_list = sorted(condition, key=lambda record: getattr(record, column_name), reverse=False)
        if len(sorted_list) is 0:
            raise EmptyFileException
        return sorted_list[0].report_date, getattr(sorted_list[0], column_name)

    @staticmethod
    def get_highest(weather_records, column_name):
        condition = [record for record in weather_records if getattr(record, column_name) is not None]
        sorted_list = sorted(condition, key=lambda record: getattr(record, column_name), reverse=True)
        if len(sorted_list) is 0:
            raise EmptyFileException
        return sorted_list[0].report_date, getattr(sorted_list[0], column_name)

    @staticmethod
    def get_average(weather_records, column_name):
        sum = 0
        count = 0
        for record in weather_records:
            if getattr(record, column_name) is not None:
                count += 1
                sum += getattr(record, column_name)
        if count is 0:
            return 0
        return sum/count


class WeatherParser(object):
    def __init__(self, path, year, month=0):
        self.file_names = []
        self.path = path
        self.year = str(year)
        self.month = month
        self.parse_file_names()

    def parse_file_names(self):
        if self.month:
            month = Util.get_month_name(self.month)
            pattern = "*{}*{}.txt".format(self.year, month)
            for file in os.listdir(os.path.basename(self.path)):
                if fnmatch.fnmatch(file, pattern):
                    self.file_names.append(file)
        else:
            for file in os.listdir(os.path.basename(self.path)):
                if fnmatch.fnmatch(file, "*{}_*.txt".format(str(self.year))):
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
            if len(row) is 0:
                continue
            if prev:
                yield prev
            prev = row


class ReportGenerator(object):
    def __init__(self, path, year, month=0):
        weather_parser = WeatherParser(path, year, month)
        self.weather_records = weather_parser.get_rows()

    def generate_extreme_condition_report(self):
        current = Weather.get_highest(self.weather_records, 'max_temp_c')
        month = current[0].strftime("%B")
        day = current[0].strftime("%d")
        print("Highest: {}C on {} {}".format(str(current[1]), month, day))
        current = Weather.get_lowest(self.weather_records, 'min_temp_c')
        month = current[0].strftime("%B")
        day = current[0].strftime("%d")
        print("Lowest: {}C on {} {}".format(str(current[1]), month, day))
        current = Weather.get_highest(self.weather_records, "max_humidity")
        month = current[0].strftime("%B")
        day = current[0].strftime("%d")
        print("Humid: {}% on {} {}".format(str(current[1]), month, day))

    def generate_average_condition_report(self):
        current = Weather.get_highest(self.weather_records, 'min_temp_c')
        print("Highest Average: {}C".format(str(current[1])))
        current = Weather.get_lowest(self.weather_records, 'min_temp_c')
        print("Lowest Average:  {}C".format(str(current[1])))
        current = Weather.get_average(self.weather_records, 'mean_humidity')
        print("Average Humidity:  {}%".format(str(current)))

    def generate_multi_line_bar_chart(self):
        first_time = True
        for record in self.weather_records:
            try:
                if first_time:
                    first_time = False
                    print(record.report_date.strftime("%B"), record.report_date.year)
                max = record.max_temp_c
                if max is None:
                    raise
                print(record.report_date.strftime("%d"), end="")
                for temp in range(0, max):
                    print("\033[91m+", end="")
                print("\033[0m", max, "C")
                min = record.min_temp_c
                print(record.report_date.strftime("%d"), end="")
                for temp in range(0, min):
                    print("\033[94m+", end="")
                print("\033[0m", str(min) + "C")
            except:
                pass

    def generate_single_line_bar_chart(self):
        first_time = True
        for record in self.weather_records:
            try:
                if first_time:
                    first_time = False
                    print(record.report_date.strftime("%B"), record.report_date.year)
                max = record.max_temp_c
                min = record.min_temp_c
                if max is None or min is None:
                    raise
                print(record.report_date.strftime("%d"), end="")
                for temp in range(0, min):
                    print("\033[94m+", end="")
                for temp in range(1, max):
                    print("\033[91m+", end="")
                print("\033[0m", str(min) + "C-" + str(max) + "C")
            except:
                pass


class Util(object):
    @staticmethod
    def get_formatted_date(date_str=""):
        date_format = "%Y-%m-%d"
        if not date_str:
            return datetime.today().date()
        return datetime.strptime(date_str, date_format).date()

    @staticmethod
    def get_month_name(month):
        date_str = "2000-{}-01".format(str(month))
        return Util.get_formatted_date(date_str).strftime("%b")


class EmptyFileException(Exception):
    def __init___(self, error):
        pass


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
    except EmptyFileException:
        print("Given Data Files are empty for selected column")
        exit(1)
    except Exception:
        print("usage: weatherman.py [-h] (-a year/month path | -s year/month path | -c year/month path | -e year path)\nweatherman.py: error correct argument is required")
        exit(1)

if __name__ == "__main__":
    main()
