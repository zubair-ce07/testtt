import sys
import os
import calendar
import re
import argparse
from HumidDayWeather import HumidDayWeather
from MaxTempDayWeather import MaxTempDayWeather
from MinTempDayWeather import MinTempDayWeather

RED_COLOR_CODE = '\033[31m'
BLUE_COLOR_CODE = '\033[34m'
GREY_COLOR_CODE = "\033[37m"


class WeatherData:
    """ Analyze Weather Data of Given DataSet """

    def __init__(self):
        self.obj_humid_day = HumidDayWeather()
        self.obj_max_day = MaxTempDayWeather()
        self.obj_min_day = MinTempDayWeather()
        self.year = 0
        self.month_name = ""

    def read_cmd_arg(self):
        """
        reads cmd line args
        """
        args_parser = argparse.ArgumentParser()
        args_parser.add_argument("dir", help="directory's path where file \
                                         to be analyzed are placed")
        args_parser.add_argument("-a", help="calculating average of max temp,\
                                        min temp and humidy of month")
        args_parser.add_argument("-e", help="calculating  max temp, min temp\
                                        and most humid day of year")
        args_parser.add_argument("-c", help="draw barhcart between low\
                                        and hight temp")
        args = args_parser.parse_args()
        if args.e:
            given_arg_list = []
            given_arg_list.append('-e')
            given_arg_list.append(args.e)
            given_arg_list.append(args.dir)
            return given_arg_list
        if args.a:
            given_arg_list = []
            given_arg_list.append('-a')
            given_arg_list.append(args.a)
            given_arg_list.append(args.dir)
            return given_arg_list
        if args.c:
            given_arg_list = []
            given_arg_list.append('-c')
            given_arg_list.append(args.c)
            given_arg_list.append(args.dir)
            return given_arg_list
        else:
            print("Invalid Arguments provided")
            exit()

    def read_file(self, file_path):
        """Reads and return file data"""
        try:
            file_reader = open(file_path, "r")
            file_data = file_reader.readlines()
            file_reader.close()
            return file_data
        except IOError:
            print "Error: can\'t find file or read data"
            exit()

    def compute_average(self, total_sum, total_elems):
        return int(total_sum / total_elems)

    def strip_invalid_chars(self, day_data):
        day_data = day_data.strip('\n\r')
        day_data = day_data.split(",")
        return day_data

    def extract_month_data(self, file_path):
        """ calculate avg temp, low temp
            and max humdity for type -a
        """
        max_temp_avg = 0
        min_temp_avg = 0
        humidity_avg = 0
        count_max_temp = 0
        count_min_temp = 0
        count_humidty = 0
        file_data = self.read_file(file_path)
        for line in file_data:
                day_data = self.strip_invalid_chars(line)
                if len(day_data) > 2:
                    if day_data[1] != "" and day_data[1] != "Max TemperatureC":
                        max_temp_avg += int(day_data[1])
                        count_max_temp += 1
                    if day_data[3] != "" and day_data[3] != "Min TemperatureC":
                        min_temp_avg += int(day_data[3])
                        count_min_temp += 1
                    if day_data[8] != "" and day_data[8] != " Mean Humidity":
                        humidity_avg += int(day_data[8])
                        count_humidty += 1
        self.obj_max_day.set_avg_max_temp(
                         self.compute_average(max_temp_avg,
                                              count_max_temp))
        self.obj_min_day.set_avg_min_temp(
                         self.compute_average(min_temp_avg,
                                              count_min_temp))
        self.obj_humid_day.set_avg_max_humidity(
                           self.compute_average(humidity_avg,
                                                count_humidty))

    def compare_max_temp(self, max_temp, day_date):
        if max_temp > self.obj_max_day.get_max_temp():
            self.obj_max_day.set_max_temp(max_temp)
            self.obj_max_day.set_max_temp_date(day_date)

    def compare_min_temp(self, min_temp, day_date):
        if min_temp < self.obj_min_day.get_min_temp():
            self.obj_min_day.set_min_temp(min_temp)
            self.obj_min_day.set_min_temp_date(day_date)

    def compare_humidity(self, day_humidity, day_date):
        if day_humidity > self.obj_humid_day.get_max_humidity():
            self.obj_humid_day.set_max_humidity(day_humidity)
            self.obj_humid_day.set_max_humidity_date(day_date)

    def extract_year_data(self, file_path):
        """ calculate max temp, low temp
            and max humdity for type -e
        """
        file_data = self.read_file(file_path)
        for line in file_data:
            day_data = self.strip_invalid_chars(line)
            if len(day_data) > 2:
                if day_data[1] != "" and day_data[1] != "Max TemperatureC":
                    self.compare_max_temp(int(day_data[1]), day_data[0])
                if day_data[3] != "" and day_data[3] != "Min TemperatureC":
                    self.compare_min_temp(int(day_data[3]), day_data[0])
                if day_data[7] != "" and day_data[7] != "Max Humidity":
                    self.compare_humidity(int(day_data[7]), day_data[0])

    def draw_barchart(self, temp, temp_color_code, day_num):
        """ draw bar chart """
        global GREY_COLOR_CODE
        counter = 0
        barchart_month = self.calc_barchart(temp)
        print(GREY_COLOR_CODE + (str(day_num)) +
              " " + (temp_color_code + barchart_month) +
              " " + (GREY_COLOR_CODE + str(temp)+"C"))

    def calc_barchart(self, temp):
        counter = 0
        barchart = ""
        while counter < temp:
            barchart += "+"
            counter += 1
        return barchart

    def calc_month_chart(self, file_path):
        global RED_COLOR_CODE
        global BLUE_COLOR_CODE
        print (self.month_name + " " + str(self.year))
        file_data = self.read_file(file_path)
        day_num = 1
        for line in file_data:
            day_data = self.strip_invalid_chars(line)
            if len(day_data) > 2:
                if day_data[1] != "" and day_data[1] != "Max TemperatureC":
                    self.draw_barchart(int(day_data[1]),
                                       RED_COLOR_CODE, day_num)
                if day_data[3] != "" and day_data[3] != "Min TemperatureC":
                    self.draw_barchart(int(day_data[3]),
                                      BLUE_COLOR_CODE, day_num)
                    day_num += 1

    def draw_bonus_barchart(self, day_num, barchart_min_temp,
                            barchart_max_temp,
                            temp_min, temp_max):
        global GREY_COLOR_CODE
        print((GREY_COLOR_CODE + str(day_num)) +
              " " + barchart_min_temp + barchart_max_temp +
              " " + (GREY_COLOR_CODE + str(temp_min) + "C-") +
              (GREY_COLOR_CODE + str(temp_max) + "C"))

    def calc_bonus_chart(self, file_path):
        """
         calculate bonus chart for max and
         low temp of each day of month
        """
        global RED_COLOR_CODE
        global BLUE_COLOR_CODE
        day_num = 1
        print ("\nBonus")
        print (self.month_name + " " + str(self.year))
        file_data = self.read_file(file_path)
        for line in file_data:
            day_data = self.strip_invalid_chars(line)
            if len(day_data) > 2:
                barchart_min_temp = ""
                barchart_max_temp = ""
                temp_max = 0
                temp_min = 0
                if day_data[1] != "" and day_data[1] != "Max TemperatureC":
                    temp_max = int(day_data[1])
                    barchart_max_temp = RED_COLOR_CODE + \
                                        self.calc_barchart(temp_max)
                if day_data[3] != "" and day_data[3] != "Min TemperatureC":
                    temp_min = int(day_data[3])
                    barchart_min_temp = BLUE_COLOR_CODE + \
                                        self.calc_barchart(temp_min)
                if day_data[3] != "Min TemperatureC" and \
                   day_data[1] != "Max TemperatureC":
                    self.draw_bonus_barchart(day_num, barchart_min_temp,
                                             barchart_max_temp,
                                             temp_min, temp_max)
                    day_num += 1
            print("")

    def check_report_type(self, valid_list_of_files):
        report_type = given_arg_list[0]
        if report_type == '-e':
            for file_path in valid_list_of_files:
                self.extract_year_data(file_path)
        elif report_type == '-a':
            self.extract_month_data(valid_list_of_files)
        elif report_type == '-c':
            self.calc_month_chart(valid_list_of_files)
            self.calc_bonus_chart(valid_list_of_files)

    def validate_given_year(self, given_year):
        if (re.match("^\d{4}$", given_year)):
            return True
        else:
            return False

    def create_year_file_path(self, given_arg_list):
        """ calculates list of files for type -a """
        files_path = given_arg_list[2]
        given_year = given_arg_list[1]
        valid_list_of_files = []
        if self.validate_given_year(given_year):
            for file_name in os.listdir(files_path):
                if given_year in file_name:
                    valid_list_of_files.append(files_path + file_name)
            return valid_list_of_files
        else:
            print("Invalid Year Given")
            exit()

    def cal_file_path(self, given_arg_list):
        """ calculate file path for type -a -c """
        year_month_list = given_arg_list[1].split("/")
        if(len(year_month_list) < 2):
            print("Wrong Second Argument Given")
            exit()
        year = year_month_list[0]
        if self.validate_given_year(year):
            self.year = year
            month_name = calendar.month_name[int(year_month_list[1])]
            self.month_name = month_name
            month_name = month_name[0:3]
            file_path = given_arg_list[2] + "lahore_weather_" + \
                        year + "_" + month_name + ".txt"
            return file_path
        else:
            print("Invalid Year Given")
            exit()

    def collect_realted_files(self, given_arg_list):
        report_type = given_arg_list[0]
        if report_type == '-e':
            if("/" in given_arg_list[1]):
                print("Wrong Argument Given")
                exit()
            return self.create_year_file_path(given_arg_list)
        elif report_type == '-a' or report_type == '-c':
            return self.cal_file_path(given_arg_list)
        else:
            print ("Wrong type given")
            exit()  # exiting program

    def print_year_temp_report(self):
        """ prints max temp, low temp
            and max humdity for type -e
        """
        # print max Temperature data
        self.obj_max_day.print_max_temp_data()
        # print min Temperature data
        self.obj_min_day.print_min_temp_data()
        # print max Humdity data
        self.obj_humid_day.print_max_humid_data()

    def print_month_temp_report(self):
        """ prints average of high, low temp
            and humdity for type -a
        """
        self.obj_max_day.print_avg_max_temp()
        self.obj_min_day.print_avg_min_temp()
        self.obj_humid_day.print_avg_max_humidity()

    def print_weather_data(self, report_type):
        """call specific method as per given output demand  """
        if report_type == '-e':
            self.print_year_temp_report()
        if report_type == '-a':
            self.print_month_temp_report()


if __name__ == "__main__":
    weather_data_obj = WeatherData()
    given_arg_list = weather_data_obj.read_cmd_arg()
    valid_list_of_files = weather_data_obj.collect_realted_files(
                          given_arg_list)
    weather_data_obj.check_report_type(valid_list_of_files)
    weather_data_obj.print_weather_data(given_arg_list[0])
