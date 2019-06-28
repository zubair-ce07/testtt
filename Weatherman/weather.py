import os
import csv
import datetime


class WeatherReading:
    def __init__(self, reading):
        self.date = self.str_to_date(reading.get("PKT", reading.get("PKST")))
        self.max_temp = int(reading["Max TemperatureC"])
        self.min_temp = int(reading["Min TemperatureC"])
        self.max_humid = int(reading["Max Humidity"])
        self.mean_humid = int(reading[" Mean Humidity"])

    @staticmethod
    def str_to_date(date):
        return datetime.datetime.strptime(date, "%Y-%m-%d")


class ResultPrinter:
    def print_annual_report(self, annual_stats):
        if not annual_stats:
            print("Record of given date not found in system")
            return
        years_max_temp = annual_stats["max temp"]
        years_min_temp = annual_stats["min temp"]
        years_max_humid = annual_stats["max humidity"]
        max_temp_date = years_max_temp.date.strftime("%B %d")
        min_temp_date = years_min_temp.date.strftime("%B %d")
        max_humid_date = years_max_humid.date.strftime("%B %d")
        print(f"\n{years_max_temp.date.year}")
        print(f"Highest: {years_max_temp.max_temp}C on {max_temp_date}")
        print(f"Lowest: {years_min_temp.min_temp}C on {min_temp_date}")
        print(f"Humidity: {years_max_humid.max_humid}% on {max_humid_date}")

    def print_monthly_report(self, month_stats, month):
        if not month_stats:
            print("Record of given date not found in system")
            return

        print(f"\n{month}")
        print(f"Highest Average: {round(month_stats['avg max temp'], 2)}C")
        print(f"Lowest Average: {round(month_stats['avg min temp'], 2)}C")
        print("Average Mean Humidity: "
              f"{round(month_stats['avg mean humidity'], 2)}%")

    def plot_month_barchart(self, chart_data):
        if not chart_data:
            print("Record of given date not found in system")
            return
        chart_month = chart_data[0].date.strftime("%B %Y")
        print(f"\n{chart_month}")
        for day_reading in chart_data:
            day = day_reading.date.strftime("%d")
            print(f"\u001b[35m{day}", end=" ")
            print(f"\u001b[31m+" * day_reading.max_temp, end=" ")
            print(f"\u001b[35m{day_reading.max_temp}C")
            print(f"\u001b[35m{day}", end=" ")
            print(f"\u001b[36m+" * day_reading.min_temp, end=" ")
            print(f"\u001b[35m{day_reading.min_temp}C", end="\n\n")

    def plot_month_horizontal_barchart(self, chart_data):
        if not chart_data:
            return
        chart_month = chart_data[0].date.strftime("%B %Y")
        print(f"\n{chart_month}")
        for day_reading in chart_data:
            day = day_reading.date.strftime("%d")
            print(f"\u001b[35m{day}", end=" ")
            print(f"\u001b[36m+" * day_reading.min_temp, end="")
            print(f"\u001b[31m+" * day_reading.max_temp, end=" ")
            print(f"\u001b[35m{day_reading.min_temp}C", end='-')
            print(f"\u001b[35m{day_reading.max_temp}C")


class WeatherAnalysis:
    @staticmethod
    def find_year_max_temp(annual_record):
        return max(annual_record, key=lambda r: r.max_temp)

    @staticmethod
    def find_year_min_temp(annual_record):
        return min(annual_record, key=lambda r: r.min_temp)

    @staticmethod
    def find_year_max_humid(annual_record):
        return max(annual_record, key=lambda r: r.max_humid)

    @staticmethod
    def find_month_avg_max_temp(month_record):
        return sum(r.max_temp for r in month_record) / len(month_record)

    @staticmethod
    def find_month_avg_min_temp(month_record):
        return sum(r.min_temp for r in month_record) / len(month_record)

    @staticmethod
    def find_month_avg_mean_humid(month_record):
        return sum(r.mean_humid for r in month_record) / len(month_record)

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
            return {}
        max_temp_record = self.find_year_max_temp(annual_record)
        min_temp_record = self.find_year_min_temp(annual_record)
        max_humid_record = self.find_year_max_humid(annual_record)
        annual_stats = {"max temp": max_temp_record,
                        "min temp": min_temp_record,
                        "max humidity": max_humid_record}

        return annual_stats

    def get_month_stats(self, weather_record, date):
        year, month = date.split("/")
        annual_record = self.find_annual_record(weather_record, year)
        if not annual_record:
            return {}
        month_record = self.find_month_record(annual_record, month)
        if not month_record:
            return {}
        avg_max_temp = self.find_month_avg_max_temp(month_record)
        avg_min_temp = self.find_month_avg_min_temp(month_record)
        avg_mean_hum = self.find_month_avg_mean_humid(month_record)
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
                           'Max Humidity',' Mean Humidity', ('PKT' or 'PKST')]
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

            return weather_record

    def parse_files(self, path):
        if not os.path.exists(path):
            print("Path not found")
            return
        weather_record = []
        files = self.read_file_names(path)
        for weather_file in files:
            weather_record += self.read_file(weather_file)

        if not weather_record:
            print("Related files not found in the directory")
            return

        return weather_record
