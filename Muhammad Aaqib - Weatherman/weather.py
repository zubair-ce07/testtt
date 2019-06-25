import os
import csv
import datetime


class WeatherReading:
    def __init__(self, date, max_temp, min_temp, max_humidity, mean_humidity):
        self.date = Reading.str_to_date(date)
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity


class ResultPrinter:
    @staticmethod
    def print_annual_report(annual_stats):
        if not annual_stats:
            ResultPrinter.print_record_not_found_message()
            return
        max_temp_obj = annual_stats["max temp"]
        min_temp_obj = annual_stats["min temp"]
        max_humidity_obj = annual_stats["max humidity"]
        max_temp = max_temp_obj.max_temp
        min_temp = min_temp_obj.min_temp
        max_humidity = max_humidity_obj.max_humidity
        max_temp_date = max_temp_obj.date.strftime("%B %d")
        min_temp_date = min_temp_obj.date.strftime("%B %d")
        max_humidity_date = max_humidity_obj.date.strftime("%B %d")
        print(f"Highest: {max_temp}C on {max_temp_date}")
        print(f"Lowest: {min_temp}C on {min_temp_date}")
        print(f"Humidity: {max_humidity}% on {max_humidity_date}")

    @staticmethod
    def print_monthly_report(month_stats):
        if not month_stats:
            ResultPrinter.print_record_not_found_message()
            return
        avg_max_temp = month_stats["avg max temp"]
        avg_min_temp = month_stats["avg min temp"]
        avg_mean_humidity = month_stats["avg mean humidity"]
        avg_max_temp = round(avg_max_temp, 2)
        avg_min_temp = round(avg_min_temp, 2)
        avg_mean_humidity = round(avg_mean_humidity, 2)
        print(f"Highest Average: {avg_max_temp}C")
        print(f"Lowest Average: {avg_min_temp}C")
        print(f"Average Mean Humidity: {avg_mean_humidity}%")

    @staticmethod
    def plot_month_barchart(chart_data):
        if not chart_data:
            ResultPrinter.print_record_not_found_message()
            return
        chart_month = chart_data[0].date.strftime("%B %Y")
        print(chart_month)
        for day_reading in chart_data:
            if not day_reading.max_temp:
                continue
            day = day_reading.date.strftime("%d")
            print(u"\u001b[35m{}".format(day), end=" ")
            print(u"\u001b[31m+" * int(day_reading.max_temp), end=" ")
            print(u"\u001b[35m{}C".format(day_reading.max_temp))
            print(u"\u001b[35m{}".format(day), end=" ")
            print(u"\u001b[36m+" * int(day_reading.min_temp), end=" ")
            print(u"\u001b[35m{}C".format(day_reading.min_temp), end="\n\n")

    @staticmethod
    def plot_component_barchart(chart_data):
        if not chart_data:
            return
        chart_month = chart_data[0].date.strftime("%B %Y")
        print(chart_month)
        for day_reading in chart_data:
            if not day_reading.min_temp:
                continue
            day = day_reading.date.strftime("%d")
            print(u"\u001b[35m{}".format(day), end=" ")
            print(u"\u001b[36m+" * int(day_reading.min_temp), end="")
            if not day_reading.max_temp:
                continue
            print(u"\u001b[31m+" * int(day_reading.max_temp), end=" ")
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


class WeatherAnalysis:
    @staticmethod
    def find_year_max_temp(annual_record):
        max_temp_obj = annual_record[0]
        for day_reading in annual_record:
            if not day_reading.max_temp:
                continue
            if int(day_reading.max_temp) > int(max_temp_obj.max_temp):
                max_temp_obj = day_reading

        return max_temp_obj

    @staticmethod
    def find_year_min_temp(annual_record):
        min_temp_obj = annual_record[0]
        for day_reading in annual_record:
            if not day_reading.min_temp:
                continue
            if int(day_reading.min_temp) < int(min_temp_obj.min_temp):
                min_temp_obj = day_reading

        return min_temp_obj

    @staticmethod
    def find_year_max_humidity(annual_record):
        max_humidity_obj = annual_record[0]
        for day_reading in annual_record:
            if not day_reading.max_humidity:
                continue
            if int(day_reading.max_humidity) > int(max_humidity_obj.
                                                   max_humidity):
                max_humidity_obj = day_reading

        return max_humidity_obj

    @staticmethod
    def find_month_avg_max_temp(month_record):
        avg_max_temp = 0
        for day_reading in month_record:
            if not day_reading.max_temp:
                    continue
            avg_max_temp += int(day_reading.max_temp)
        avg_max_temp /= len(month_record)

        return avg_max_temp

    @staticmethod
    def find_month_avg_min_temp(month_record):
        avg_min_temp = 0
        for day_reading in month_record:
            if not day_reading.min_temp:
                    continue
            avg_min_temp += int(day_reading.min_temp)
        avg_min_temp /= len(month_record)

        return avg_min_temp

    @staticmethod
    def find_month_avg_mean_humidity(month_record):
        avg_mean_humidity = 0
        for day_reading in month_record:
            if not day_reading.mean_humidity:
                    continue
            avg_mean_humidity += int(day_reading.mean_humidity)
        avg_mean_humidity /= len(month_record)

        return avg_mean_humidity

    @staticmethod
    def find_annual_record(weather_record, year):
        annual_record = []
        for day_reading in weather_record:
            reading_date = day_reading.date
            reading_year = reading_date.strftime("%Y")
            if reading_year == year:
                annual_record.append(day_reading)

        return annual_record

    @staticmethod
    def find_month_record(annual_record, month):
        month_record = []
        for day_reading in annual_record:
            reading_date = day_reading.date
            reading_month = reading_date.strftime("%m")
            if reading_month == month:
                month_record.append(day_reading)

        return month_record

    @staticmethod
    def get_annual_stats(weather_record, year):
        annual_record = WeatherAnalysis.find_annual_record(weather_record,
                                                           year)
        if not annual_record:
            return
        max_temp_data = WeatherAnalysis.find_year_max_temp(annual_record)
        min_temp_data = WeatherAnalysis.find_year_min_temp(annual_record)
        max_humidity_data = WeatherAnalysis.find_year_max_humidity(
                            annual_record)
        annual_stats = {"max temp": max_temp_data,
                        "min temp": min_temp_data,
                        "max humidity": max_humidity_data}

        return annual_stats

    @staticmethod
    def get_month_stats(weather_record, date):
        year, month = date.split("/")
        annual_record = WeatherAnalysis.find_annual_record(weather_record,
                                                           year)
        if not annual_record:
            return
        month_record = WeatherAnalysis.find_month_record(annual_record, month)
        if not month_record:
            return
        avg_max_temp = WeatherAnalysis.find_month_avg_max_temp(month_record)
        avg_min_temp = WeatherAnalysis.find_month_avg_min_temp(month_record)
        avg_mean_hum = WeatherAnalysis.find_month_avg_mean_humidity(
                       month_record)
        month_stats = {"avg max temp": avg_max_temp,
                       "avg min temp": avg_min_temp,
                       "avg mean humidity": avg_mean_hum}

        return month_stats

    @staticmethod
    def get_chart_data(weather_record, date):
        year, month = date.split("/")
        annual_record = WeatherAnalysis.find_annual_record(weather_record,
                                                           year)
        if not annual_record:
            return
        month_record = WeatherAnalysis.find_month_record(annual_record, month)
        if not month_record:
            return

        return month_record


class FileParser:
    def __init__(self):
        self.file_found = False

    @staticmethod
    def read_file_names(path):
        files = []
        for root, _, weather_file in os.walk(path):
            for file in weather_file:
                if '.txt' in file:
                    files.append(os.path.join(root, file))

        return files

    def read_file_tuple(self, row):
        if 'Max TemperatureC' not in row or 'Min TemperatureC' not in row or \
           'Max Humidity' not in row or ' Mean Humidity' not in row or \
           ('PKT' not in row and 'PKST' not in row):
                return

        self.file_found = True
        max_temp = row['Max TemperatureC']
        min_temp = row['Min TemperatureC']
        max_humidity = row['Max Humidity']
        mean_humidity = row[' Mean Humidity']
        date = row["PKT"] if "PKT" in row else row["PKST"]
        row_readings = WeatherReading(date, max_temp, min_temp,
                                      max_humidity, mean_humidity)

        return row_readings

    def read_file(self, weather_file, weather_record):
        with open(weather_file, newline='') as csvfile:
            reading = csv.DictReader(csvfile)
            for row in reading:
                row_readings = self.read_file_tuple(row)
                weather_record.append(row_readings)

    def parse_file(self, path):
        if not os.path.exists(path):
            ResultPrinter.print_path_not_found_message()
            return

        weather_record = []
        files = FileParser.read_file_names(path)
        for weather_file in files:
            self.read_file(weather_file, weather_record)

        if not self.file_found:
            ResultPrinter.print_file_not_found_message()
            return

        return weather_record


class Reading:
    @staticmethod
    def str_to_date(date):
        year, month, day = date.split("-")
        date = datetime.date(int(year), int(month), int(day))
        return date
