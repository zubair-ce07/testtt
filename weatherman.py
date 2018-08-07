import sys
import os
import calendar
import re
import enum
import argparse
from DayWeather import DayWeather


class ColorCode(enum.Enum):
    RED = '\033[31m'
    BLUE = '\033[34m'
    GREY = "\033[37m"


class ForecastReport:
    """ Analyze Weather Data of Given DataSet """

    def __init__(self):
        self.obj_day_weather = DayWeather()

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
        given_arg_list = []
        if args.e:
            given_arg_list.append('-e')
            given_arg_list.append(args.e)
        elif args.a:
            given_arg_list.append('-a')
            given_arg_list.append(args.a)
        elif args.c:
            given_arg_list.append('-c')
            given_arg_list.append(args.c)
        else:
            print("Invalid Arguments provided")
            exit()
        given_arg_list.append(args.dir)
        return given_arg_list

    def read_file(self, file_path):
        """Reads and return file data"""
        try:
            file_reader = open(file_path, "r")
            file_data = file_reader.readlines()
            file_reader.close()
            return file_data
        except IOError:
            print ("Error: can\'t find file or read data")
            exit()

    def compute_average(self, total_sum, total_elems):
        return int(total_sum / total_elems)

    def strip_invalid_chars(self, day_data):
        day_data = day_data.strip('\n\r')
        day_data = day_data.split(",")
        return day_data

    def check_valid_year_month_file(self, day_date, year_month):
         match = re.search(r'\d\d\d\d', day_date)
         if match:
             day_date_list = day_date.split("-")
             year_month_list = year_month.split("/")
             if (day_date_list[0] == year_month_list[0]) and (day_date_list[1] == year_month_list[1]):
                 return True
             else:
                 return False
         else:
             return False

    def extract_month_data(self, file_path, year_month):
        """ calculate avg temp, low temp
            and max humdity for type -a
        """
        max_temp_avg = 0
        min_temp_avg = 0
        humidity_avg = 0
        count_max_temp = 0
        count_min_temp = 0
        count_humidty = 0
        correct_files = False
        file_data = self.read_file(file_path)
        for line in file_data:
                day_data = self.strip_invalid_chars(line)
                if self.check_valid_year_month_file(day_data[0], year_month) == False:
                    continue
                if self.check_valid_year_month_file(day_data[0], year_month) == True:
                    correct_files = True
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
        if correct_files:
            self.obj_day_weather.set_avg_max_temp(
                             self.compute_average(max_temp_avg,
                                                  count_max_temp))
            self.obj_day_weather.set_avg_min_temp(
                             self.compute_average(min_temp_avg,
                                                  count_min_temp))
            self.obj_day_weather.set_avg_max_humidity(
                               self.compute_average(humidity_avg,
                                                    count_humidty))

    def compare_max_temp(self, max_temp, day_date):
        if max_temp > self.obj_day_weather.get_max_temp():
            self.obj_day_weather.set_max_temp(max_temp)
            self.obj_day_weather.set_max_temp_date(day_date)

    def compare_min_temp(self, min_temp, day_date):
        if min_temp < self.obj_day_weather.get_min_temp():
            self.obj_day_weather.set_min_temp(min_temp)
            self.obj_day_weather.set_min_temp_date(day_date)

    def compare_humidity(self, day_humidity, day_date):
        if day_humidity > self.obj_day_weather.get_max_humidity():
            self.obj_day_weather.set_max_humidity(day_humidity)
            self.obj_day_weather.set_max_humidity_date(day_date)

    def check_valid_year_file(self, day_date,year):
         match = re.search(r'\d\d\d\d', day_date)
         if match and (year in day_date):
             return True
         else:
             return False



    def extract_year_data(self, file_path,year):
        """ calculate max temp, low temp
            and max humdity for type -e
        """
        file_data = self.read_file(file_path)
        for line in file_data:
            day_data = self.strip_invalid_chars(line)
            if self.check_valid_year_file(day_data[0], year):
                if len(day_data) > 2:
                    if day_data[1] != "" and day_data[1] != "Max TemperatureC":
                        self.compare_max_temp(int(day_data[1]), day_data[0])
                    if day_data[3] != "" and day_data[3] != "Min TemperatureC":
                        self.compare_min_temp(int(day_data[3]), day_data[0])
                    if day_data[7] != "" and day_data[7] != "Max Humidity":
                        self.compare_humidity(int(day_data[7]), day_data[0])


    def draw_barchart(self, temp, temp_color_code, day_num):
        """ draw bar chart """
        counter = 0
        barchart_month = self.calc_barchart(temp)
        print(ColorCode.GREY.value + (str(day_num)) +
              " " + (temp_color_code + barchart_month) +
              " " + (ColorCode.GREY.value  + str(temp)+"C"))

    def calc_barchart(self, temp):
        counter = 0
        barchart = ""
        while counter < temp:
            barchart += "+"
            counter += 1
        return barchart

    def calc_month_chart(self, file_path, year_month):
        file_data = self.read_file(file_path)
        day_num = 1
        for line in file_data:
            day_data = self.strip_invalid_chars(line)
            if self.check_valid_year_month_file(day_data[0], year_month) == False:
                continue
            if len(day_data) > 2:
                if day_data[1] != "" and day_data[1] != "Max TemperatureC":
                    self.draw_barchart(int(day_data[1]),
                                       ColorCode.RED.value, day_num)
                if day_data[3] != "" and day_data[3] != "Min TemperatureC":
                    self.draw_barchart(int(day_data[3]),
                                      ColorCode.BLUE.value, day_num)
                    day_num += 1

    def draw_bonus_barchart(self, day_num, barchart_min_temp,
                            barchart_max_temp,
                            temp_min, temp_max):
        print((ColorCode.GREY.value + str(day_num)) +
              " " + barchart_min_temp + barchart_max_temp +
              " " + (ColorCode.GREY.value + str(temp_min) + "C-") +
              (ColorCode.GREY.value + str(temp_max) + "C"))

    def calc_bonus_chart(self, file_path, year_month):
        """
         calculate bonus chart for max and
         low temp of each day of month
        """
        day_num = 1
        file_data = self.read_file(file_path)
        for line in file_data:
            day_data = self.strip_invalid_chars(line)
            if self.check_valid_year_month_file(day_data[0], year_month) == False:
                continue
            if len(day_data) > 2:
                barchart_min_temp = ""
                barchart_max_temp = ""
                temp_max = 0
                temp_min = 0
                if day_data[1] != "" and day_data[1] != "Max TemperatureC":
                    temp_max = int(day_data[1])
                    barchart_max_temp = ColorCode.RED.value + \
                                        self.calc_barchart(temp_max)
                if day_data[3] != "" and day_data[3] != "Min TemperatureC":
                    temp_min = int(day_data[3])
                    barchart_min_temp = ColorCode.BLUE.value + \
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
                self.extract_year_data(file_path, given_arg_list[1])
        elif report_type == '-a':
            for file_path in valid_list_of_files:
                self.extract_month_data(file_path, given_arg_list[1])
        elif report_type == '-c':
            for file_path in valid_list_of_files:
                self.calc_month_chart(file_path, given_arg_list[1])
            print("\nBonus\n")
            for file_path in valid_list_of_files:
                self.calc_bonus_chart(file_path, given_arg_list[1])

    def validate_given_year(self, given_arg_list):
        report_type = given_arg_list[0]
        given_year = given_arg_list[1]
        if report_type == '-e':
            if (re.match("^\d{4}$", given_year) and ("/" not in given_year)):
                return True
            else:
                return False
        elif report_type == '-a' or report_type == '-c':
            year_month_list = given_arg_list[1].split("/")
            year = year_month_list[0]
            if(len(year_month_list) == 2) and (re.match("^\d{4}$", year)):
                return True
            else:
                return False

    def collect_files(self, files_path):
        valid_list_of_files = []
        for file_name in os.listdir(files_path):
            valid_list_of_files.append(files_path + file_name)
        return valid_list_of_files

    def collect_files_list(self, given_arg_list):
        report_type = given_arg_list[0]
        valid_list_of_files = []
        if report_type == '-e':
            if self.validate_given_year(given_arg_list):
                valid_list_of_files = self.collect_files(given_arg_list[2])
            else:
                print("Wrong Argument Given")
                exit()
        elif report_type == '-a' or report_type == '-c':
            if self.validate_given_year(given_arg_list):
                valid_list_of_files = self.collect_files(given_arg_list[2])
            else:
                print("Wrong Argument Given")
                exit()
        else:
            print ("Wrong type given")
            exit()  # exiting program
        return valid_list_of_files

    def print_year_temp_report(self):
        """ prints max temp, low temp
            and max humdity for type -e
        """
        # print max Temperature data
        self.obj_day_weather.print_max_temp_data()
        # print min Temperature data
        self.obj_day_weather.print_min_temp_data()
        # print max Humdity data
        self.obj_day_weather.print_max_humid_data()

    def print_month_temp_report(self):
        """ prints average of high, low temp
            and humdity for type -a
        """
        self.obj_day_weather.print_avg_max_temp()
        self.obj_day_weather.print_avg_min_temp()
        self.obj_day_weather.print_avg_max_humidity()

    def print_weather_data(self, report_type):
        """call specific method as per given output demand  """
        if report_type == '-e':
            self.print_year_temp_report()
        if report_type == '-a':
            self.print_month_temp_report()


if __name__ == "__main__":
    weather_data_obj = ForecastReport()
    given_arg_list = weather_data_obj.read_cmd_arg()
    list_of_files = weather_data_obj.collect_files_list(
                          given_arg_list)
    weather_data_obj.check_report_type(list_of_files)
    weather_data_obj.print_weather_data(given_arg_list[0])
