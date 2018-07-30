import sys
import os
import datetime


class WeatherData():
    """"""
    max_temp = 0
    min_temp = 100
    max_humidity = 0
    max_temp_date = ""
    min_temp_date = ""
    max_humidity_date = ""
    month_dictionary = {1: 'January',
                        2: 'February',
                        3: 'March',
                        4: 'April',
                        5: 'May',
                        6: 'Jun',
                        7: 'July',
                        8: 'August',
                        9: 'September',
                        10: 'October',
                        11: 'November',
                        12: 'December'
                        }

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

    def extract_data(self, file_path):
        file_reader = open(file_path, "r")
        file_data = file_reader.readlines()
        file_reader.close()
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

    def read_files(self, valid_list_of_files):
        for file_path in valid_list_of_files:
            self.extract_data(file_path)
        # self.extract_data(valid_list_of_files[0])

    def year_temp_report(self, sgiven_arg_list):
        files_path = given_arg_list[2]
        given_year = given_arg_list[1]
        valid_list_of_files = []
        for file_name in os.listdir(files_path):
            if given_year in file_name:
                valid_list_of_files.append(files_path + file_name)
        return valid_list_of_files

    def collect_realted_files(self, given_arg_list):
        report_type = given_arg_list[0]
        if report_type == '-e':
            return self.year_temp_report(given_arg_list)
        elif report_type == '-a':
            pass
        elif report_type == '-c':
            pass
        else:
            print ("Wrong type given")
            exit()  # exiting program

    def print_weather_data(self):
        max_temp_date = self.max_temp_date.split("-")
        min_temp_date = self.min_temp_date.split("-")
        max_humidity_date = self.max_temp_date.split("-")
        # print max Temperature data
        print("Highest: " + str(self.max_temp) +
              "C on " + self.month_dictionary[int(max_temp_date[1])] +
              " " + str(max_temp_date[2]))
        # print min Temperature data
        print("Lowest: " + str(self.min_temp) +
              "C on " + self.month_dictionary[int(min_temp_date[1])] +
              " " + str(min_temp_date[2]))
        # print max Humdity data
        print("Humid: " + str(self.max_humidity) +
              "% on " + self.month_dictionary[int(max_humidity_date[1])] +
              " " + str(max_humidity_date[2]))


if __name__ == "__main__":
    weather_data_obj = WeatherData()
    given_arg_list = weather_data_obj.read_cmd_arg()
    valid_list_of_files =
    weather_data_obj.collect_realted_files(given_arg_list)
    weather_data_obj.read_files(valid_list_of_files)
    weather_data_obj.print_weather_data()
