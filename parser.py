import json
from weather import WeatherReading
from column_attribute_association import associations


class WeatherParser():
    """Parses weather readings from CSV file to WeatherReading objects"""

    def __get_parameters(self, raw_weather_readings):
        """Returns class attributes with which WeatherReading object is initialized with"""
        parameters = {}
        for key in associations:
            index = associations[key]["column_position"]
            parameters[key] = raw_weather_readings[index]
        return parameters

    def __parse_column_names(self, raw_weather_readings):
        """Returns column names from the CSV file"""
        column_names = raw_weather_readings[0].split(',')
        column_names = [c.strip() for c in column_names]
        return column_names

    def __parse_rows(self, raw_weather_readings):
        """Returns array of data rows from the CSV file"""
        data_rows = raw_weather_readings[1:]
        data_rows = [row.split(',') for row in data_rows]
        return data_rows

    def parse_weather_file(self, file):
        """Returns WeatherReading objects after parsing the weather reading CSV file"""
        with open(file, 'r') as weather_file:
            raw_weather_readings = weather_file.read().strip().split('\n')

            if raw_weather_readings[-1][0:4] == "<!--":
                raw_weather_readings = raw_weather_readings[0:-1]

            data_rows = self.__parse_rows(raw_weather_readings)

            objects = []

            for data_row in data_rows:
                parameters = self.__get_parameters(data_row)
                raw_weather_readings_object = WeatherReading(**parameters)
                objects.append(raw_weather_readings_object)

        return objects