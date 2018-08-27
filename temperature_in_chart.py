"""
this module displays monthly temperature of a month in a bar chart
"""
from calendar import month_abbr, month_name
import glob
import utils
from read_csv import ReadCsv


class TemperatureInChart:
    """
        this class displays weather data in chart
    """

    def __init__(self, two_line_chart=False, one_line_chart=False):
        self.two_line_chart = two_line_chart
        self.one_line_chart = one_line_chart

    def display_two_line_chart(self, file_path):
        """
        :param file_path:
        :return: none
        displays the daily temperture of a month
        """

        csv_reader = ReadCsv(file_path)
        read_csv = csv_reader.read_csv_file()

        for row in read_csv:
            day = row['PKT'].split("-")[2]
            if row['Max TemperatureC']:
                max_temp = int(row['Max TemperatureC'])
                max_temp_string = ""
                for index in range(max_temp):
                    max_temp_string = max_temp_string + "+"
                print("%s \033[0;31m%s\033[0;m %dC" % (day, max_temp_string, max_temp))
            if row['Min TemperatureC']:
                min_temp = int(row['Min TemperatureC'])
                min_temp_string = ""
                for index in range(min_temp):
                    min_temp_string = min_temp_string + "-"
                print("%s \033[0;34m%s\033[0;m %dC" % (day, min_temp_string, min_temp))

    def display_one_line_chart(self, file_path):
        """
        :param file_path:
        :return: none
        display horizontally the temperatures of the month
        """
        csv_reader = ReadCsv(file_path)
        read_csv = csv_reader.read_csv_file()
        for row in read_csv:
            max_temp_flag = False
            min_temp_flag = False
            max_temp_string = ""
            min_temp_string = ""
            max_temp = 0
            min_temp = 0
            day = row['PKT'].split("-")[2]
            if row['Max TemperatureC']:
                max_temp = int(row['Max TemperatureC'])

                max_temp_flag = True
                for index in range(max_temp):
                    max_temp_string = max_temp_string + "+"
            if row['Min TemperatureC']:
                min_temp = int(row['Min TemperatureC'])

                min_temp_flag = True
                for index in range(min_temp):
                    min_temp_string = min_temp_string + "-"
            if max_temp_flag or min_temp_flag:
                print("%s \033[0;34m%s\033[0;m\033[0;31m%s\033[0;m  %dC - %dC"
                      % (day, min_temp_string, max_temp_string,
                         min_temp, max_temp))

    def display_temperature_in_chart(self, date_str, dir_path):
        """
        this method displays emperature in chart according to type
        :param date_str:
        :param dir_path:
        :return:
        """
        (year, month) = date_str.split('/')
        month = int(month)
        file_path = glob.glob(dir_path + "/*_" + year + "_" + month_abbr[month] + "*")
        if file_path:
            file_path = file_path[0]
            print("%s %s" % (month_name[month], year))
            if self.two_line_chart:
                self.display_two_line_chart(file_path)
            elif self.one_line_chart:
                self.display_one_line_chart(file_path)
        else:
            print("No Data Found for the Specified Month")
