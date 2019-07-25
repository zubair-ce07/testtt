import csv
import glob
import calendar

from weather import WeatherReading


class WeatherParser:
    """Parses weather readings from CSV file to WeatherReading objects"""

    def parse_weather_files(self, readings_dir, year, month=0):
        """Returns WeatherReading objects after parsing the weather reading CSV file"""
        file_paths = f"{readings_dir}/*{year}*{calendar.month_abbr[month]}*"
        file_paths = glob.glob(file_paths)

        objects = []

        for file_path in file_paths:
            with open(file_path, 'r') as weather_file:
                next(weather_file) # discard empty line at top
                weather_reading_rows = csv.DictReader(weather_file)

                for row in weather_reading_rows:
                    if "PKT" in row:
                        if row['PKT'][0:4] == "<!--":  # check if row is not a comment
                            continue
                    if "PSKT" in row:
                        if row['PSKT'][0:4] == "<!--":  # check if row is not a comment
                            continue
                    raw_weather_readings_object = WeatherReading(row)
                    objects.append(raw_weather_readings_object)
        return objects
