import csv
import io
import zipfile
import argparse
import datetime
import reports
from enum import Enum
from weatherreading import WeatherReading


class ReportType(Enum):
    YEARLY = 1
    MONTHLY = 2
    MONTHLY_WITH_CHART = 3


class WeatherMan:

    def __init__(self, filepath):
        self.filepath = filepath
        self.weather_readings = []

    def get_weather_data(self, file_name):
        zip_archive = zipfile.ZipFile(self.filepath, 'r')
        self.weather_readings = []
        for file in zip_archive.infolist():
            zip_file_name = file.filename
            file_match = zip_file_name.find(file_name)
            if file_match != -1:
                csv_file = zip_archive.open(zip_file_name, mode='r')
                csv_file = io.TextIOWrapper(csv_file)
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    reading_date_value = row['PKT']
                    max_temperature_c_value = None if row['Max TemperatureC'] == '' else int(row['Max TemperatureC'])
                    min_temperature_c_value = None if row['Min TemperatureC'] == '' else int(row['Min TemperatureC'])
                    max_humidity_value = None if row['Max Humidity'] == '' else int(row['Max Humidity'])
                    mean_humidity_value = None if row[' Mean Humidity'] == '' else int(row[' Mean Humidity'])
                    self.weather_readings.append(WeatherReading(reading_date_value, max_temperature_c_value,
                                                                min_temperature_c_value, max_humidity_value,
                                                                mean_humidity_value))
        return self.weather_readings

    def parse_input(self, input_data):
        year_month_date = None
        file_name = None
        report_type = ReportType.YEARLY
        try:
            year_month_date = datetime.datetime.strptime(input_data, '%Y/%m')
            report_type = ReportType.MONTHLY
        except ValueError:
            try:
                year_month_date = datetime.datetime.strptime(input_data, '%Y')
                report_type = ReportType.YEARLY
            except ValueError:
                print("Invalid data entered")
                return

        if report_type == ReportType.MONTHLY:
            month_name = year_month_date.strftime('%b')
            year_name = year_month_date.strftime('%Y')
            file_name = year_name + "_" + month_name
        elif report_type == ReportType.YEARLY:
            year_name = year_month_date.strftime('%Y')
            file_name = year_name

        return self.get_weather_data(file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="weather data file path")
    parser.add_argument("-e", help="For a given year display the highest temperature and day,"
                                   " lowest temperature and day, most humid day and humidity.")
    parser.add_argument("-a", help="For a given month display the average highest temperature, "
                                   "average lowest temperature, average mean humidity.")
    parser.add_argument("-c", help="For a given month draw two horizontal bar charts on the console for the highest "
                                   "and lowest temperature on each day. Highest in red and lowest in blue.")
    args = parser.parse_args()
    weatherMan = None

    if args.filepath:
        weatherMan = WeatherMan(filepath=args.filepath)

    if args.e:
        weatherMan.parse_input(input_data=args.e)
        if len(weatherMan.weather_readings) != 0:
            reports.generate_report(report_type=1, weather_readings=weatherMan.weather_readings)
        else:
            print('no data found')

    if args.a:
        weatherMan.parse_input(input_data=args.a)
        if len(weatherMan.weather_readings) != 0:
            reports.generate_report(report_type=2, weather_readings=weatherMan.weather_readings)
        else:
            print('no data found')

    if args.c:
        weatherMan.parse_input(input_data=args.c)
        if len(weatherMan.weather_readings) != 0:
            reports.generate_report(report_type=3, weather_readings=weatherMan.weather_readings)
        else:
            print('no data found')
