import sys
import os
import calendar


class WeatherData():
    """ Analyze Weather Datas Given DataSet """
    max_temp = 0
    min_temp = 100
    max_humidity = 0
    avg_max_temp = 0
    avg_min_temp = 0
    avg_max_humidity = 0
    max_temp_date = ""
    min_temp_date = ""
    max_humidity_date = ""
    year = 0
    month_name = ""
    red_color_code = '\033[31m'
    blue_color_code = '\033[34m'
    grey_color_code = "\033[37m"

    def read_cmd_arg(self, *argv):
        """
        reads cmd line args
        """
        if len(sys.argv) == 4:
            given_arg_list = []
            given_arg_list.append(sys.argv[1])
            given_arg_list.append(sys.argv[2])
            given_arg_list.append(sys.argv[3])
            return given_arg_list
        else:
            print('Wrong Arguments Provided')
            exit()  # exiting program

    def read_file(self, file_path):
        """Reads and return file data"""
        file_reader = open(file_path, "r")
        file_data = file_reader.readlines()
        file_reader.close()
        return file_data

    def extract_data_month(self, file_path):
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
                day_data = line.strip('\n\r')
                day_data = day_data.split(",")
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
        self.avg_max_temp = int(max_temp_avg/count_max_temp)
        self.avg_min_temp = int(min_temp_avg/count_min_temp)
        self.avg_max_humidity = int(humidity_avg/count_humidty)

    def extract_data_year(self, file_path):
        """ calculate max temp, low temp
            and max humdity for type -e
        """
        file_data = self.read_file(file_path)
        for line in file_data:
                day_data = line.strip('\n\r')
                day_data = day_data.split(",")
                if len(day_data) > 2:
                    if day_data[1] != "" and day_data[1] != "Max TemperatureC":
                        max_temp = int(day_data[1])
                        if max_temp > self.max_temp:
                            self.max_temp = max_temp
                            self.max_temp_date = day_data[0]
                    if day_data[3] != "" and day_data[3] != "Min TemperatureC":
                        min_temp = int(day_data[3])
                        if min_temp < self.min_temp:
                            self.min_temp = min_temp
                            self.min_temp_date = day_data[0]
                    if day_data[7] != "" and day_data[7] != "Max Humidity":
                        day_humidity = int(day_data[7])
                        if day_humidity > self.max_humidity:
                            self.max_humidity = day_humidity
                            self.max_humidity_date = day_data[0]

    def draw_barchart(self, temp, temp_color_code, day_num):
        """ draw bar chart """
        counter = 0
        barchart_month = self.calc_barchart(temp)
        print(self.grey_color_code + (str(day_num)) +
              " " + (temp_color_code + barchart_month) +
              " " + (self.grey_color_code + str(temp)+"C"))

    def calc_barchart(self, temp):
        counter = 0
        barchart = ""
        while counter < temp:
            barchart += "+"
            counter += 1
        return barchart

    def calc_month_chart(self, file_path):
        print (self.month_name + " " + str(self.year))
        file_data = self.read_file(file_path)
        day_num = 1
        for line in file_data:
            day_data = line.strip('\n\r')
            day_data = day_data.split(",")
            if len(day_data) > 2:
                if day_data[1] != "" and day_data[1] != "Max TemperatureC":
                    self.draw_barchart(int(day_data[1]),
                         self.red_color_code, day_num)
                if day_data[3] != "" and day_data[3] != "Min TemperatureC":
                    self.draw_barchart(int(day_data[3]),
                         self.blue_color_code, day_num)
                    day_num += 1

    def draw_bnous_barchart(self, day_num, barchart_min_temp,
                            barchart_max_temp,
                            temp_min, temp_max):
        print((self.grey_color_code + str(day_num)) +
              " " + barchart_min_temp + barchart_max_temp +
              " " + (self.grey_color_code + str(temp_min) + "C-") +
              (self.grey_color_code + str(temp_max) + "C"))

    def calc_bonus_chart(self, file_path):
        """
         calculate bonus chart for max and
         low temp of each day of month
        """
        print (self.month_name + " " + str(self.year))
        day_num = 1
        file_data = self.read_file(file_path)
        for line in file_data:
            day_data = line.strip('\n\r')
            day_data = day_data.split(",")
            if len(day_data) > 2:
                words = line.split(",")
                barchart_min_temp = ""
                barchart_max_temp = ""
                temp_max = 0
                temp_min = 0
                if day_data[1] != "" and day_data[1] != "Max TemperatureC":
                    temp_max = int(day_data[1])
                    barchart_max_temp = self.red_color_code + \
                                        self.calc_barchart(temp_max)
                if day_data[3] != "" and day_data[3] != "Min TemperatureC":
                    temp_min = int(day_data[3])
                    barchart_min_temp = self.blue_color_code + \
                                        self.calc_barchart(temp_min)
                if day_data[3] != "Min TemperatureC" and day_data[1] != "Max TemperatureC":
                    self.draw_bnous_barchart(day_num, barchart_min_temp,
                                             barchart_max_temp,
                                             temp_min, temp_max)
                    day_num += 1
            print("")

    def check_report_type(self, valid_list_of_files):
        report_type = given_arg_list[0]
        if report_type == '-e':
            for file_path in valid_list_of_files:
                self.extract_data_year(file_path)
        elif report_type == '-a':
            self.extract_data_month(valid_list_of_files)
        elif report_type == '-c':
            self.calc_month_chart(valid_list_of_files)
            print ("\nBonus")
            self.calc_bonus_chart(valid_list_of_files)

    def year_temp_report(self, given_arg_list):
        """ calculates list of files for type -a """
        files_path = given_arg_list[2]
        given_year = given_arg_list[1]
        valid_list_of_files = []
        for file_name in os.listdir(files_path):
            if given_year in file_name:
                valid_list_of_files.append(files_path + file_name)
        return valid_list_of_files

    def cal_file_path(self, given_arg_list):
        """ calculate file path for type -a -c """
        year_month_list = given_arg_list[1].split("/")
        if(len(year_month_list) < 2):
            print("Wrong Second Argument Given")
            exit()
        year = year_month_list[0]
        self.year = year
        month_name = calendar.month_name[int(year_month_list[1])]
        self.month_name = month_name
        month_name = month_name[0:3]
        file_path = given_arg_list[2] + "lahore_weather_" + \
                    year + "_" + month_name + ".txt"
        return file_path

    def collect_realted_files(self, given_arg_list):
        report_type = given_arg_list[0]
        if report_type == '-e':
            if("/" in given_arg_list[1]):
                print("Wrong Argument Given")
                exit()
            return self.year_temp_report(given_arg_list)
        elif report_type == '-a':
            return self.cal_file_path(given_arg_list)
        elif report_type == '-c':
            return self.cal_file_path(given_arg_list)
        else:
            print ("Wrong type given")
            exit()  # exiting program

    def print_year_temp_report(self):
        """ prints max temp, low temp
            and max humdity for type -e
        """
        max_temp_date = self.max_temp_date.split("-")
        min_temp_date = self.min_temp_date.split("-")
        max_humidity_date = self.max_temp_date.split("-")
        # print max Temperature data
        print("Highest: " + str(self.max_temp) +
              "C on " + calendar.month_name[int(max_temp_date[1])] +
              " " + str(max_temp_date[2]))
        # print min Temperature data
        print("Lowest: " + str(self.min_temp) +
              "C on " + calendar.month_name[int(min_temp_date[1])] +
              " " + str(min_temp_date[2]))
        # print max Humdity data
        print("Humid: " + str(self.max_humidity) +
              "% on " + calendar.month_name[int(max_humidity_date[1])] +
              " " + str(max_humidity_date[2]))

    def print_month_temp_report(self):
        """ prints average of high, low temp
            and humdity for type -a
        """
        print ("Highest Average: " + str(self.avg_max_temp) + "C")
        print ("Lowest Average: " + str(self.avg_min_temp) + "C")
        print ("Average Humidity: " + str(self.avg_max_humidity) + "%")

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
