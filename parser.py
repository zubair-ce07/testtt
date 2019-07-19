import csv
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

    def parse_weather_file(self, file):
        """Returns WeatherReading objects after parsing the weather reading CSV file"""
        with open(file, 'r') as weather_file:
            raw_weather_readings = csv.reader(weather_file)

            # skip the headers
            next(raw_weather_readings)  
            next(raw_weather_readings)  

            objects = []

            for row in raw_weather_readings:
                if(row):
                    if row[0][0:4] == "<!--":
                        continue

                    parameters = self.__get_parameters(row)
                    raw_weather_readings_object = WeatherReading(**parameters)
                    objects.append(raw_weather_readings_object)


        return objects
