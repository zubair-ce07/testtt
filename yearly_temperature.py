import os.path
import utilities
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
            if row['Max TemperatureC'] != '':
                hight_temp = int(row['Max TemperatureC'])
                if hight_temp > self.highest:
                    self.highest = hight_temp
                    self.highest_temp_day = row['PKT']
            if row['Min TemperatureC'] != '':
                low_temp = int(row['Min TemperatureC'])
                if low_temp < self.lowest:
                    self.lowest = low_temp
                    self.lowest_temp_day = row['PKT']
            if row['Max Humidity'] != '':
                humidity = int(row['Max Humidity'])
                if humidity > self.humidity:
                    self.humidity = humidity
                    self.humid_day = row['PKT']

    def show_yearly_temperature(self, date_str, file_path):
        """
        this method show yearly temperature
        :param date_str:
        :param file_path:
        :return:
        """
        date_str = date_str.split('/')
        # here is used indexing because other method was not effective for this
        year = date_str[0]
        for index in range(1, 13):
            file_path = file_path+"/"+constants.FILE_START_NAME+year+"_" + \
                   utilities.get_month_abbr(index) + constants.FILE_EXTENSION
            if os.path.exists(file_path):
                self.find_yearly_temperature(file_path)

        if self.highest != constants.MIN_VALUE:
            print("Highest: %dC on %s" % (
                self.highest,
                utilities.get_formatted_date(self.highest_temp_day)))
        else:
            print("No Record of Highest Temperature Found for This Year")
        if self.lowest != constants.MAX_VALUE:
            print("Lowest: %dC on %s" % (
                self.lowest,
                utilities.get_formatted_date(self.lowest_temp_day)))
        else:
            print("No Record of Lowest Temperature Found for This Year")
        if self.humid_day != "":
            print("Humid: %d%% on %s" % (
                self.humidity,
                utilities.get_formatted_date(self.humid_day)))
        else:
            print("No Record of Humidity Found for This Year")
