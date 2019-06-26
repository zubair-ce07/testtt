import csv
import logging

from WeatherReading import WeatherReading


class Parser:
    @staticmethod
    def read_file(path):
        """This function will receive a pth+filename and returns a list of weather obj of that file
        if the file isn't found, it will log a warning.
        """
        reading_list = list()
        try:
            with open(path) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    reading = WeatherReading(
                        (row['PKST' if 'PKST' in row.keys() else 'PKT']),
                        row['Max TemperatureC'],
                        row['Min TemperatureC'],
                        row['Max Humidity'],
                        row[' Mean Humidity'])
                    reading_list.append(reading)
        except IOError:
            logging.warning(path + ' Not found')
        except TypeError as e:
            print(e)
        return reading_list
