import glob
import csv


class PopulateWeatherData:

    def __init__(self, dir_path, year, month):
        self.directory_path = dir_path
        self.year = year
        self.month = month
        self.list_of_weather_details = []

    def populate(self):
        for file in glob.glob('{}/*{}*{}.txt'.format(self.directory_path, self.year, self.month)):
            with open(file) as csvfile:
                weather_details = csv.DictReader(csvfile)
                for row in weather_details:
                    weather_record = self.verify_data(row)
                    self.list_of_weather_details.append(weather_record)

    def verify_data(self, weather_records):
        for weather_record in weather_records:
            if not weather_records[weather_record]:
                weather_records[weather_record] = None
        return weather_records
