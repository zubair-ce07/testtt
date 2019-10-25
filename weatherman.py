import csv
import io
import zipfile
import argparse
import datetime
from reporttype import ReportType
import reports
from weatherreading import WeatherReading
from constants import Constants


class WeatherMan:

    def __init__(self, filepath):
        self.filepath = filepath
        self.weather_readings = []

    def get_weather_data(self, file_name):
        zip_archive = zipfile.ZipFile(self.filepath, Constants.FILE_READ_MODE)
        self.weather_readings = []
        for file in zip_archive.infolist():
            zip_file_name = file.filename
            file_match = zip_file_name.find(file_name)
            if file_match != Constants.INVALID_DATA:
                csv_file = zip_archive.open(zip_file_name, mode=Constants.FILE_READ_MODE)
                csv_file = io.TextIOWrapper(csv_file)
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    reading_date_value = row[Constants.READING_TIME_INDEX]
                    max_temperature_c_value = Constants.INVALID_DATA if row[Constants.READING_MAX_TEMP_C_INDEX] == \
                                                                        Constants.EMPTY_STRING \
                        else int(row[Constants.READING_MAX_TEMP_C_INDEX])

                    min_temperature_c_value = Constants.INVALID_DATA if row[Constants.READING_MIN_TEMP_C_INDEX] == \
                                                                        Constants.EMPTY_STRING \
                        else int(row[Constants.READING_MIN_TEMP_C_INDEX])

                    max_humidity_value = Constants.INVALID_DATA if row[Constants.READING_MAX_HUMIDITY_INDEX] == \
                                                                   Constants.EMPTY_STRING \
                        else int(row[Constants.READING_MAX_HUMIDITY_INDEX])

                    mean_humidity_value = Constants.INVALID_DATA if row[Constants.READING_MEAN_HUMIDITY_INDEX] == \
                                                                    Constants.EMPTY_STRING \
                        else int(row[Constants.READING_MEAN_HUMIDITY_INDEX])

                    self.weather_readings.append(WeatherReading(reading_date_value, max_temperature_c_value,
                                                                min_temperature_c_value, max_humidity_value,
                                                                mean_humidity_value))
        return self.weather_readings

    def parse_input(self, input_data):
        year_month_date = None
        file_name = None
        report_type = ReportType.YEARLY
        try:
            year_month_date = datetime.datetime.strptime(input_data, Constants.DATE_YEAR_AND_MONTH_FORMAT)
            report_type = ReportType.MONTHLY
        except ValueError:
            try:
                year_month_date = datetime.datetime.strptime(input_data, Constants.DATE_YEAR_FORMAT)
                report_type = ReportType.YEARLY
            except ValueError:
                print(Constants.INVALID_DATA_MESSAGE)
                return

        if report_type == ReportType.MONTHLY:
            month_name = year_month_date.strftime(Constants.DATE_MONTH_FORMAT)
            year_name = year_month_date.strftime(Constants.DATE_YEAR_FORMAT)
            file_name = year_name + Constants.DATE_YEAR_AND_MONTH_SEPARATOR + month_name
        elif report_type == ReportType.YEARLY:
            year_name = year_month_date.strftime(Constants.DATE_YEAR_FORMAT)
            file_name = year_name

        return self.get_weather_data(file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(Constants.FILE_PATH_ARGUMENT, help=Constants.FILE_PATH_ARGUMENT_MESSAGE)
    parser.add_argument(Constants.YEAR_ARGUMENT, help=Constants.YEAR_ARGUMENT_MESSAGE)
    parser.add_argument(Constants.MONTH_ARGUMENT, help=Constants.MONTH_ARGUMENT_MESSAGE)
    parser.add_argument(Constants.MONTH_CHART_ARGUMENT, help=Constants.MONTH_CHART_ARGUMENT_MESSAGE)
    args = parser.parse_args()
    weatherMan = None

    if args.filepath:
        weatherMan = WeatherMan(filepath=args.filepath)

    if args.e:
        weatherMan.parse_input(input_data=args.e)
        if len(weatherMan.weather_readings) != 0:
            reports.generate_report(report_type=ReportType.YEARLY.value, weather_readings=weatherMan.weather_readings)
        else:
            print(Constants.NO_DATA_FOUND_MESSAGE)

    if args.a:
        weatherMan.parse_input(input_data=args.a)
        if len(weatherMan.weather_readings) != 0:
            reports.generate_report(report_type=ReportType.MONTHLY.value, weather_readings=weatherMan.weather_readings)
        else:
            print(Constants.NO_DATA_FOUND_MESSAGE)

    if args.c:
        weatherMan.parse_input(input_data=args.c)
        if len(weatherMan.weather_readings) != 0:
            reports.generate_report(report_type=ReportType.MONTHLY_WITH_CHART.value,
                                    weather_readings=weatherMan.weather_readings)
        else:
            print(Constants.NO_DATA_FOUND_MESSAGE)
