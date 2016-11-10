from WeatherData import WeatherData


class WeatherDataParser(object):
    # Constants for Positions/Indices of fields in data file
    DATE = 0
    MAX_TEMPERATURE = 1
    MEAN_TEMPERATURE = 2
    MIN_TEMPERATURE = 3
    MAX_HUMIDITY = 6
    MEAN_HUMIDITY = 7
    MIN_HUMIDITY = 8

    def __init__(self, directory):
        self.directory = directory
        self.data = []

    def parse_data(self):
        from myfunctions import get_files
        from myfunctions import map_to_weather_obj
        from functools import reduce
        files = get_files(self.directory)
        weather_objects = []
        for file in files:
            with open(file) as f:
                data = f.readlines()[1:]  # Skip first line of the file
                objs = list(map(lambda line: map_to_weather_obj(line), data))
                weather_objects.append(objs)

        self.data = reduce(list.__add__, weather_objects)

    def get_data(self):
        return self.data


def map_to_weather_obj(line):
    values = line.split(',')

    return WeatherData(date=values[WeatherDataParser.DATE],
                       max_temp=values[WeatherDataParser.MAX_TEMPERATURE],
                       mean_temp=values[WeatherDataParser.MEAN_TEMPERATURE],
                       min_temp=values[WeatherDataParser.MIN_TEMPERATURE],
                       max_humidity=values[WeatherDataParser.MAX_HUMIDITY],
                       mean_humidity=values[WeatherDataParser.MEAN_HUMIDITY],
                       min_humidity=values[WeatherDataParser.MIN_HUMIDITY])
