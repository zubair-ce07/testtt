import os
import csv
import datetime


class WeatherReading:
    def __init__(self, reading):
        self.date = Reading.str_to_date(reading.get("PKT") or
                                        reading.get("PKST"))
        self.max_temp = int(reading["Max TemperatureC"])
        self.min_temp = int(reading["Min TemperatureC"])
        self.max_humidity = int(reading["Max Humidity"])
        self.mean_humidity = int(reading[" Mean Humidity"])


class ResultPrinter:
    def print_annual_report(self, annual_stats):
        if not annual_stats:
            self.print_record_not_found_message()
            return
        max_temp_reading = annual_stats["max temp"]
        min_temp_reading = annual_stats["min temp"]
        max_humidity_reading = annual_stats["max humidity"]
        max_temp_date = max_temp_reading.date.strftime("%B %d")
        min_temp_date = min_temp_reading.date.strftime("%B %d")
        max_humidity_date = max_humidity_reading.date.strftime("%B %d")
        print(f"\n{max_temp_reading.date.year}")
        print(f"Highest: {max_temp_reading.max_temp}C on {max_temp_date}")
        print(f"Lowest: {min_temp_reading.min_temp}C on {min_temp_date}")
        print("Humidity: {}% on {}".format(max_humidity_reading.max_humidity,
              max_humidity_date))

    def print_monthly_report(self, month_stats, month):
        if not month_stats:
            self.print_record_not_found_message()
            return
        avg_max_temp = month_stats["avg max temp"]
        avg_min_temp = month_stats["avg min temp"]
        avg_mean_humidity = month_stats["avg mean humidity"]
        print(f"\n{month}")
        print(f"Highest Average: {round(avg_max_temp, 2)}C")
        print(f"Lowest Average: {round(avg_min_temp, 2)}C")
        print(f"Average Mean Humidity: {round(avg_mean_humidity, 2)}%")

    def plot_month_barchart(self, chart_data):
        if not chart_data:
            self.print_record_not_found_message()
            return
        chart_month = chart_data[0].date.strftime("%B %Y")
        print(f"\n{chart_month}")
        for day_reading in chart_data:
            day = day_reading.date.strftime("%d")
            print(u"\u001b[35m{}".format(day), end=" ")
            print(u"\u001b[31m+" * day_reading.max_temp, end=" ")
            print(u"\u001b[35m{}C".format(day_reading.max_temp))
            print(u"\u001b[35m{}".format(day), end=" ")
            print(u"\u001b[36m+" * day_reading.min_temp, end=" ")
            print(u"\u001b[35m{}C".format(day_reading.min_temp), end="\n\n")

    def plot_component_barchart(self, chart_data):
        if not chart_data:
            return
        chart_month = chart_data[0].date.strftime("%B %Y")
        print(f"\n{chart_month}")
        for day_reading in chart_data:
            day = day_reading.date.strftime("%d")
            print(u"\u001b[35m{}".format(day), end=" ")
            print(u"\u001b[36m+" * day_reading.min_temp, end="")
            print(u"\u001b[31m+" * day_reading.max_temp, end=" ")
            print(u"\u001b[35m{}C".format(day_reading.min_temp), end='-')
            print(u"\u001b[35m{}C".format(day_reading.max_temp))

    @staticmethod
    def print_record_not_found_message():
        print("Record of given year/month does not exists in the system")

    @staticmethod
    def print_file_not_found_message():
        print("Related files not found in the given directory")

    @staticmethod
    def print_path_not_found_message():
        print("Path to directory not found")

    @staticmethod
    def print_invalid_month_message():
        print("Invalid month format. Use yyyy/mm")


class WeatherAnalysis:
    @staticmethod
    def find_year_max_temp(annual_record):
        return max(annual_record, key=lambda r: r.max_temp)

    @staticmethod
    def find_year_min_temp(annual_record):
        return min(annual_record, key=lambda r: r.min_temp)

    @staticmethod
    def find_year_max_humidity(annual_record):
        return max(annual_record, key=lambda r: r.max_humidity)

    @staticmethod
    def find_month_avg_max_temp(month_record):
        return sum(r.max_temp for r in month_record) / len(month_record)

    @staticmethod
    def find_month_avg_min_temp(month_record):
        return sum(r.min_temp for r in month_record) / len(month_record)

    @staticmethod
    def find_month_avg_mean_humidity(month_record):
        return sum(r.mean_humidity for r in month_record) / len(month_record)

    @staticmethod
    def find_annual_record(weather_record, year):
        return [reading for reading in weather_record
                if reading.date.year == int(year)]

    @staticmethod
    def find_month_record(annual_record, month):
        return [reading for reading in annual_record
                if reading.date.month == int(month)]

    def get_annual_stats(self, weather_record, year):
        annual_record = self.find_annual_record(weather_record, year)
        if not annual_record:
            return
        max_temp_data = self.find_year_max_temp(annual_record)
        min_temp_data = self.find_year_min_temp(annual_record)
        max_humidity_data = self.find_year_max_humidity(annual_record)
        annual_stats = {"max temp": max_temp_data,
                        "min temp": min_temp_data,
                        "max humidity": max_humidity_data}

        return annual_stats

    def get_month_stats(self, weather_record, date):
        year, month = date.split("/")
        annual_record = self.find_annual_record(weather_record, year)
        if not annual_record:
            return
        month_record = self.find_month_record(annual_record, month)
        if not month_record:
            return
        avg_max_temp = self.find_month_avg_max_temp(month_record)
        avg_min_temp = self.find_month_avg_min_temp(month_record)
        avg_mean_hum = self.find_month_avg_mean_humidity(month_record)
        month_stats = {"avg max temp": avg_max_temp,
                       "avg min temp": avg_min_temp,
                       "avg mean humidity": avg_mean_hum}

        return month_stats

    def get_chart_data(self, weather_record, date):
        year, month = date.split("/")
        annual_record = self.find_annual_record(weather_record, year)
        if not annual_record:
            return
        month_record = self.find_month_record(annual_record, month)
        if not month_record:
            return

        return month_record


class FileParser:
    @staticmethod
    def is_valid_reading(reading):
        required_fields = ['Max TemperatureC', 'Min TemperatureC',
                           'Max Humidity',' Mean Humidity', ("PKT" or "PKST")]
        return all(reading.get(field) for field in required_fields)

    @staticmethod
    def read_file_names(path):
        files = []
        for file in os.listdir(path):
            file = os.path.join(path, file)
            if os.path.isfile(file) and 'txt' in file:
                files.append(file)

        return files

    def read_file(self, weather_file):
        weather_record = []
        with open(weather_file, newline='') as csvfile:
            reading = csv.DictReader(csvfile)
            weather_record += [WeatherReading(row) for row in reading
                               if self.is_valid_reading(row)]

            return (weather_record)

    def parse_files(self, path):
        if not os.path.exists(path):
            ResultPrinter.print_path_not_found_message()
            return
        weather_record = []
        files = FileParser.read_file_names(path)
        for weather_file in files:
            weather_record += self.read_file(weather_file)

        if not weather_record:
            ResultPrinter.print_file_not_found_message()
            return

        return weather_record


class Reading:
    @staticmethod
    def str_to_date(date):
        year, month, day = date.split("-")
        date = datetime.date(int(year), int(month), int(day))
        return date
