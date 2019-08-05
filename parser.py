import csv
import glob
import calendar

from weather import WeatherReading


class WeatherParser:
    """Parses weather readings from CSV file to WeatherReading objects"""

    def _is_row_valid(self, row):
        date = row.get('PKT', row.get('PKST'))
        if "<!--" in date:  # check if row is not a comment
            return False
        return True

    def parse_weather_files(self, readings_dir, year, month=0):
        """Returns WeatherReading objects after parsing the weather reading CSV file"""
        file_paths = f"{readings_dir}/*{year}*{calendar.month_abbr[month]}*"
        file_paths = glob.glob(file_paths)

        weather_readings = []

        for file_path in file_paths:
            with open(file_path, 'r') as weather_file:
                next(weather_file)  # discard empty line at top
                rows = csv.DictReader(weather_file)

                readings = [WeatherReading(row)
                            for row in rows if self._is_row_valid(row)]

                weather_readings.extend(readings)

        return weather_readings
