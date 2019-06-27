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
            logging.error(path + ' Not found')
        except TypeError as e:
            print(e)
        return reading_list

    @staticmethod
    def date_tokenizer(date):
        tokenize_date = date.split('/')
        if len(tokenize_date) < 2:
            logging.error('few Arguments\nProper format is year/month')
            exit(0)
        if int(tokenize_date[0]) not in range(2004, 2017):
            logging.error('Year must between 2004 - 2016')
            exit(0)
        if int(tokenize_date[1]) not in range(1, 13):
            logging.error('Month must between 1 - 12')
            exit(0)
        return tokenize_date[0], tokenize_date[1]
