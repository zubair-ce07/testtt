import csv
from weather import WeatherReading


class WeatherParser():
    """Parses weather readings from CSV file to WeatherReading objects"""

    def parse_weather_file(self, file):
        """Returns WeatherReading objects after parsing the weather reading CSV file"""
        with open(file, 'r') as weather_file:
            next(weather_file) # discard empty line at top
            weather_reading_rows = csv.DictReader(weather_file)

            objects = []

            for row in weather_reading_rows:
                    try:
                        if row['PKT'][0:4] != "<!--":  # check if row is valid
                            raw_weather_readings_object = WeatherReading(**row)
                            objects.append(raw_weather_readings_object)
                    except KeyError:
                        continue
        return objects
