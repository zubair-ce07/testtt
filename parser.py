import csv
import glob
import calendar
from weather import WeatherReading


class WeatherParser:
    """Parses weather readings from CSV file to WeatherReading objects"""

    @staticmethod
    def parse_weather_files(readings_dir, year, month=0):
        """Returns WeatherReading objects after parsing the weather reading CSV file"""
        file_paths = "{}/*{}*{}*".format(readings_dir, year, calendar.month_abbr[month])
        file_paths = glob.glob(file_paths)

        objects = []

        for file_path in file_paths:
            with open(file_path, 'r') as weather_file:
                next(weather_file) # discard empty line at top
                weather_reading_rows = csv.DictReader(weather_file)

                for row in weather_reading_rows:
                        try:
                            if row['PKT'][0:4] != "<!--":  # check if row is valid
                                raw_weather_readings_object = WeatherReading(**row)
                                objects.append(raw_weather_readings_object)
                        except KeyError:
                            continue
        return objects
