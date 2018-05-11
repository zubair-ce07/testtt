import os.path
import csv
import calendar
from collections import namedtuple

class WeatherParser:

    weather_record = namedtuple('Weather', ('date, max_temp, min_temp, max_humidity, mean_humidity'))


    def generate_yearly_filename(self, year, directory):
        return [directory + '/Murree_weather_' + year + '_' + calendar.month_abbr[int(months_count)] \
                + '.txt' for months_count in range(12)]

    def generate_monthly_filename(self, date, directory):
        weather_date = date.split("/")
        filename = directory + '/Murree_weather_' + weather_date[0] + '_' \
                   + calendar.month_abbr[int(weather_date[1])] + '.txt'
        return filename

    def read_weather_file(self, filepath):
        weather_fields = ['Max TemperatureC','Min TemperatureC','Max Humidity',' Mean Humidity']

        weather_readings = []
        if not os.path.exists(filepath):
            return None
        with open (filepath) as weatherfile:
            reader = csv.DictReader(weatherfile)
            for row in reader:
                if not all(row.get(fields) for fields in weather_fields):
                    continue
                weather_readings += [self.weather_record(row.get('PKT') or row.get('PKST'),
                                        int(row['Max TemperatureC']), int(row['Min TemperatureC']),
                                        int(row['Max Humidity']), int(row[' Mean Humidity']))]

        return weather_readings
