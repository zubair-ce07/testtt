import csv
import io
import zipfile
import argparse
from datetime import datetime
from weather_man.reporttype import ReportType
from weather_man import reports
from weather_man.weatherreading import WeatherReading
from weather_man.weathermanconstants import WeatherManConstants


class WeatherMan:

    def __init__(self, filepath):
        self.filepath = filepath
        self.weather_readings = []

    def get_weather_data(self, file_name):
        zip_archive = zipfile.ZipFile(self.filepath, WeatherManConstants.FILE_READ_MODE)
        self.weather_readings = []
        for file in zip_archive.infolist():
            zip_file_name = file.filename
            file_match = zip_file_name.find(file_name)
            if file_match != WeatherManConstants.INVALID_DATA:
                csv_file = zip_archive.open(zip_file_name, mode=WeatherManConstants.FILE_READ_MODE)
                csv_file = io.TextIOWrapper(csv_file)
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    reading_date_value = row[WeatherManConstants.READING_TIME_INDEX]
                    max_temperature_c_value = WeatherManConstants.INVALID_DATA \
                        if row[WeatherManConstants.READING_MAX_TEMP_C_INDEX] == WeatherManConstants.EMPTY_STRING \
                        else int(row[WeatherManConstants.READING_MAX_TEMP_C_INDEX])

                    min_temperature_c_value = WeatherManConstants.INVALID_DATA \
                        if row[WeatherManConstants.READING_MIN_TEMP_C_INDEX] == WeatherManConstants.EMPTY_STRING \
                        else int(row[WeatherManConstants.READING_MIN_TEMP_C_INDEX])

                    max_humidity_value = WeatherManConstants.INVALID_DATA \
                        if row[WeatherManConstants.READING_MAX_HUMIDITY_INDEX] == WeatherManConstants.EMPTY_STRING \
                        else int(row[WeatherManConstants.READING_MAX_HUMIDITY_INDEX])

                    mean_humidity_value = WeatherManConstants.INVALID_DATA \
                        if row[WeatherManConstants.READING_MEAN_HUMIDITY_INDEX] == WeatherManConstants.EMPTY_STRING \
                        else int(row[WeatherManConstants.READING_MEAN_HUMIDITY_INDEX])

                    self.weather_readings.append(WeatherReading(reading_date_value, max_temperature_c_value,
                                                                min_temperature_c_value, max_humidity_value,
                                                                mean_humidity_value))
        return self.weather_readings

    def parse_input(self, input_data):
        file_name = None
        try:
            year_month_date = datetime.strptime(input_data, WeatherManConstants.DATE_YEAR_AND_MONTH_FORMAT)
            report_type = ReportType.MONTHLY
        except ValueError:
            try:
                year_month_date = datetime.strptime(input_data, WeatherManConstants.DATE_YEAR_FORMAT)
                report_type = ReportType.YEARLY
            except ValueError:
                print(WeatherManConstants.INVALID_DATA_MESSAGE)
                return

        if report_type == ReportType.MONTHLY:
            month_name = year_month_date.strftime(WeatherManConstants.DATE_MONTH_FORMAT)
            year_name = year_month_date.strftime(WeatherManConstants.DATE_YEAR_FORMAT)
            file_name = year_name + WeatherManConstants.DATE_YEAR_AND_MONTH_SEPARATOR + month_name
        elif report_type == ReportType.YEARLY:
            year_name = year_month_date.strftime(WeatherManConstants.DATE_YEAR_FORMAT)
            file_name = year_name

        return self.get_weather_data(file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(WeatherManConstants.FILE_PATH_ARGUMENT, help=WeatherManConstants.FILE_PATH_ARGUMENT_MESSAGE)
    parser.add_argument(WeatherManConstants.YEAR_ARGUMENT, help=WeatherManConstants.YEAR_ARGUMENT_MESSAGE)
    parser.add_argument(WeatherManConstants.MONTH_ARGUMENT, help=WeatherManConstants.MONTH_ARGUMENT_MESSAGE)
    parser.add_argument(WeatherManConstants.MONTH_CHART_ARGUMENT, help=WeatherManConstants.MONTH_CHART_ARGUMENT_MESSAGE)
    args = parser.parse_args()
    weatherMan = None

    if args.filepath:
        weatherMan = WeatherMan(filepath=args.filepath)

    if args.e:
        weatherMan.parse_input(input_data=args.e)
        if len(weatherMan.weather_readings) != 0:
            reports.generate_report(report_type=ReportType.YEARLY.value, weather_readings=weatherMan.weather_readings)
        else:
            print(WeatherManConstants.NO_DATA_FOUND_MESSAGE)

    if args.a:
        weatherMan.parse_input(input_data=args.a)
        if len(weatherMan.weather_readings) != 0:
            reports.generate_report(report_type=ReportType.MONTHLY.value, weather_readings=weatherMan.weather_readings)
        else:
            print(WeatherManConstants.NO_DATA_FOUND_MESSAGE)

    if args.c:
        weatherMan.parse_input(input_data=args.c)
        if len(weatherMan.weather_readings) != 0:
            reports.generate_report(report_type=ReportType.MONTHLY_WITH_CHART.value,
                                    weather_readings=weatherMan.weather_readings)
        else:
            print(WeatherManConstants.NO_DATA_FOUND_MESSAGE)
