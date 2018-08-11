import os.path
import constants
import utilities
from read_csv import ReadCsv


class AverageTemperatue:
    """ Class for storing Average Temperatures """
    def __init__(self):
        self.average_high = constants.ZERO
        self.average_low = constants.ZERO
        self.average_humidity = constants.ZERO

    def find_average_temperature(self, file_path):
        """
        This function take file path and return the
        AverageTemperature object
        """
        high_count = constants.ZERO
        low_count = constants.ZERO
        humid_count = constants.ZERO
        csv_reader = ReadCsv(file_path)
        read_csv = csv_reader.read_csv_file()

        for row in read_csv:
            if row['Max TemperatureC'] != '':
                self.average_high += int(row['Max TemperatureC'])
                high_count += 1
            if row['Min TemperatureC'] != '':
                self.average_low += int(row['Min TemperatureC'])
                low_count += 1
            if row[' Mean Humidity'] != '':
                self.average_humidity += int(row[' Mean Humidity'])
                humid_count += 1

        self.average_high = self.average_high / high_count
        self.average_low = self.average_low / low_count
        self.average_humidity = self.average_humidity / humid_count

    def show_average_temperature(self, date_str, file_path):
        """
        this function is for displaying average temperature
        :param date_str:
        :param file_path:
        :return: none
        """
        (year, month)=date_str.split('/')
        month = int(month)
        file_path = file_path + "/" + constants.FILE_START_NAME + year + "_" +\
                    utilities.get_month_abbr(month) + constants.FILE_EXTENSION

        if os.path.exists(file_path):
            self.find_average_temperature(file_path)

            print("%s %s" % (utilities.get_month_name(month), year))
            print("Highest Average: %dC" % self.average_high)
            print("Lowest Average: %dC" % self.average_low)
            print("Average Humidity: %d%%" % self.average_humidity)
        else:
            print("No Data Found for the Specified Month")
