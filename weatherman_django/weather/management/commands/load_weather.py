"""
this module contains a django command that read data from  files from a directory and save it into
 Database
"""
import glob
import csv
import logging
from django.core.management.base import BaseCommand

from weather.models import Weather, City, WeatherCharacteristics

logger = logging.getLogger("weather_logger")


class Command(BaseCommand):
    """
    this is a custom django command to store weather data from files to DB
    """
    help = 'Read the weather data from csv files present at the directory that you specify' \
           ' and save that data into database'

    def add_arguments(self, parser):
        """
        this method defines the command line arguments required for this command
        :param parser:
        :return:
        """
        parser.add_argument("dir_path", help="Path of Weather Data Directory", type=str)

    def handle(self, *args, **options):
        """
        when command is called, this method will handle it and work accordingly
        :param args:
        :param options:
        :return:
        """
        dir_path = options['dir_path']
        files_path = glob.glob(dir_path + "/*weather*[.txt|.csv]")

        if not files_path:
            # it should be printed on console as it tells whether the data directory was correct
            # or not
            self.stdout.write("No Weather files found so no data is added\n")
            return
        for file_path in files_path:
            city_name = file_path.split('/')[-1].split('_')[0]
            city, status = City.objects.get_or_create(name=city_name)
            read_csv_and_save_data(file_path, city)

        # it should be printed on console as it tells whether the data is synced or not
        self.stdout.write("Added the new data to DB and does not changed the old data\n")


def read_csv_and_save_data(file_path, city):
    """
    this function read weather data from CSV file given in file_path and save that data in DB
    :param file_path:
    :param city:
    :return:
    """
    with open(file_path) as csvfile:
        weather_data_csv = csv.DictReader(csvfile, delimiter=',')
        for row in weather_data_csv:
            weather_date = None
            if 'PKT' in row:
                weather_date = row['PKT']
            elif 'PKST' in row:
                weather_date = row['PKST']
            else:
                return
            try:
                weather = Weather.objects.get(date=weather_date, city=city)
                logger.info("already present")
            except:
                logger.info("adding new")
                weather = Weather()
                weather.date = weather_date
                try:
                    # setting temperatures
                    max_value = None
                    if row['Max TemperatureC']:
                        max_value = float(row['Max TemperatureC'])
                    mean_value = None
                    if row['Mean TemperatureC']:
                        mean_value = float(row['Mean TemperatureC'])
                    min_value = None
                    if row['Min TemperatureC']:
                        min_value = float(row['Min TemperatureC'])
                    weather.temperature = WeatherCharacteristics(max_value=max_value,
                                                                 mean_value=mean_value,
                                                                 min_value=min_value)
                    weather.temperature.save()
                    weather.temperature = weather.temperature

                    # setting Dew Point
                    max_value = None
                    if row['Dew PointC']:
                        max_value = float(row['Dew PointC'])
                    mean_value = None
                    if row['MeanDew PointC']:
                        mean_value = float(row['MeanDew PointC'])
                    min_value = None
                    if row['Min DewpointC']:
                        min_value = float(row['Min DewpointC'])
                    weather.dew_point = WeatherCharacteristics(max_value=max_value,
                                                               mean_value=mean_value,
                                                               min_value=min_value)
                    weather.dew_point.save()

                    # setting Humidity
                    max_value = None
                    if row['Max Humidity']:
                        max_value = float(row['Max Humidity'])
                    mean_value = None
                    if row[' Mean Humidity']:
                        mean_value = float(row[' Mean Humidity'])
                    min_value = None
                    if row[' Min Humidity']:
                        min_value = float(row[' Min Humidity'])
                    weather.humidity = WeatherCharacteristics(max_value=max_value,
                                                              mean_value=mean_value,
                                                              min_value=min_value)
                    weather.humidity.save()

                    # setting Sea Level Pressure
                    max_value = None
                    if row[' Max Sea Level PressurehPa']:
                        max_value = float(row[' Max Sea Level PressurehPa'])
                    mean_value = None
                    if row[' Mean Sea Level PressurehPa']:
                        mean_value = float(row[' Mean Sea Level PressurehPa'])
                    min_value = None
                    if row[' Min Sea Level PressurehPa']:
                        min_value = float(row[' Min Sea Level PressurehPa'])
                    weather.sea_pressure = WeatherCharacteristics(max_value=max_value,
                                                                  mean_value=mean_value,
                                                                  min_value=min_value)
                    weather.sea_pressure.save()

                    # setting Visibility
                    max_value = None
                    if row[' Max VisibilityKm']:
                        max_value = float(row[' Max VisibilityKm'])
                    mean_value = None
                    if row[' Mean VisibilityKm']:
                        mean_value = float(row[' Mean VisibilityKm'])
                    min_value = None
                    if row[' Min VisibilitykM']:
                        min_value = float(row[' Min VisibilitykM'])
                    weather.visibility = WeatherCharacteristics(max_value=max_value,
                                                                mean_value=mean_value,
                                                                min_value=min_value)
                    weather.visibility.save()

                    # setting Wind Speed
                    max_value = None
                    if row[' Max Wind SpeedKm/h']:
                        max_value = float(row[' Max Wind SpeedKm/h'])
                    mean_value = None
                    if row[' Mean Wind SpeedKm/h']:
                        mean_value = float(row[' Mean Wind SpeedKm/h'])

                    weather.wind = WeatherCharacteristics(max_value=max_value,
                                                          mean_value=mean_value)
                    weather.wind.save()

                    weather.max_gust_speed = None
                    if row[' Max Gust SpeedKm/h']:
                        weather.max_gust_speed = int(row[' Max Gust SpeedKm/h'])
                    weather.precipitation = None
                    if row['Precipitationmm']:
                        weather.precipitation = float(row['Precipitationmm'])
                    weather.cloud_cover = None
                    if row[' CloudCover']:
                        weather.cloud_cover = int(row[' CloudCover'])
                    weather.events = None
                    if row[' Events']:
                        weather.events = row[' Events']
                    weather.wind_dir_degrees = None
                    if row['WindDirDegrees']:
                        weather.wind_dir_degrees = int(row['WindDirDegrees'])
                    weather.city = city

                    # i don't know why i have to do this but without it, data wasn't saving
                    weather.temperature = weather.temperature
                    weather.dew_point = weather.dew_point
                    weather.humidity = weather.humidity
                    weather.sea_pressure = weather.sea_pressure
                    weather.visibility = weather.visibility
                    weather.wind = weather.wind
                    weather.save()
                except:
                    logger.error(
                        "some error occured so data of date: %s could not be saved" % weather_date)
