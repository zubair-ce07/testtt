import glob
import csv


class PopulateWeatherData:

    def __init__(self, dir_path, year, month):
        self.directory_path = dir_path
        self.year = year
        self.month = month
        self.list_of_weather_details = []

    # Populates the list of weather dictionaries from a specified path.
    def populate(self):

        for file in glob.glob('%s/*_%s_%s.txt' % (self.directory_path, self.year, self.month)):
            with open(file) as csvfile:
                weather_details = csv.DictReader(csvfile)
                dict = {}
                for row in weather_details:
                    dict = self.verify_data(row)
                    self.list_of_weather_details.append(dict)

    # This methods add None value to key which has no value
    def verify_data(self, weather_dictionary):

        for item in weather_dictionary:
            if not weather_dictionary[item]:
                weather_dictionary[item] = None

        return weather_dictionary

