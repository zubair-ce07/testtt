import csv
from weather import WeatherReading
from column_attribute_association import associations


class WeatherParser():
    """Parses weather readings from CSV file to WeatherReading objects"""

    def __get_parameters(self, weather_reading_row):
        """Returns class attributes with which WeatherReading object is initialized with"""
        parameters = {}
        for key in associations:
            index = associations[key]["column_position"]
            parameters[key] = weather_reading_row[index]
        return parameters

    def parse_weather_file(self, file):
        """Returns WeatherReading objects after parsing the weather reading CSV file"""
        with open(file, 'r') as weather_file:
            weather_reading_rows = csv.reader(weather_file)

            # skip the headers
            next(weather_reading_rows)  
            next(weather_reading_rows)  

            objects = []

            for row in weather_reading_rows:
                if(row):
                    if row[0][0:4] == "<!--":
                        continue

                    parameters = self.__get_parameters(row)
                    raw_weather_readings_object = WeatherReading(**parameters)
                    objects.append(raw_weather_readings_object)


        return objects
