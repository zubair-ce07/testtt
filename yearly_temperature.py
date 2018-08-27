"""
this module calculate and show yearly temperature of a given year
"""
from calendar import month_abbr
import glob
from datetime import datetime
import constants
from read_csv import ReadCsv


class YearlyTemperature:
    """ This is a class for storing Yearly Temperature """
    def __init__(self):
        self.highest = constants.MIN_VALUE
        self.highest_temp_day = constants.EMPTY_STRING
        self.lowest = constants.MAX_VALUE
        self.lowest_temp_day = constants.EMPTY_STRING
        self.humidity = constants.ZERO
        self.humid_day = constants.EMPTY_STRING

    def find_yearly_temperature(self, file_path):
        """
        this method find yearly tepmerature
        :param file_path:
        :return:
        """
        csv_reader = ReadCsv(file_path)
        read_csv = csv_reader.read_csv_file()
        for row in read_csv:
            if row['Max TemperatureC']:
                hight_temp = int(row['Max TemperatureC'])
                if hight_temp > self.highest:
                    self.highest = hight_temp
                    self.highest_temp_day = row['PKT']
            if row['Min TemperatureC']:
                low_temp = int(row['Min TemperatureC'])
                if low_temp < self.lowest:
                    self.lowest = low_temp
                    self.lowest_temp_day = row['PKT']
            if row['Max Humidity']:
                humidity = int(row['Max Humidity'])
                if humidity > self.humidity:
                    self.humidity = humidity
                    self.humid_day = row['PKT']

    def show_yearly_temperature(self, date_str, dir_path):
        """
        this method show yearly temperature
        :param date_str:
        :param dir_path:
        :return:
        """
        date_str = date_str.split('/')
        # here is used indexing because other method was not effective for this
        year = date_str[0]
        for index in range(1, 13):
            file_path = glob.glob(dir_path + "/*_" + year + "_" + month_abbr[index] + "*")

            if file_path:
                file_path = file_path[0]
                self.find_yearly_temperature(file_path)

        if self.highest != constants.MIN_VALUE:
            print("Highest: %dC on %s" % (
                self.highest,
                datetime.strptime(self.highest_temp_day, "%Y-%m-%d").strftime("%b %d")))
        else:
            print("No Record of Highest Temperature Found for This Year")
        if self.lowest != constants.MAX_VALUE:
            print("Lowest: %dC on %s" % (
                self.lowest,
                datetime.strptime(self.lowest_temp_day, "%Y-%m-%d").strftime("%b %d")))
        else:
            print("No Record of Lowest Temperature Found for This Year")
        if self.humid_day:
            print("Humid: %d%% on %s" % (
                self.humidity,
                datetime.strptime(self.humid_day, "%Y-%m-%d").strftime("%b %d")))
        else:
            print("No Record of Humidity Found for This Year")
