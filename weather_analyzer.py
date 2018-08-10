import os
from day_weather import DayWeather
import re
from color_codes import ColorCode


class WeatherAnalyzer:
    def __init__(self):
        self.day_weather_list = []

    def collect_files(self, files_path):
        list_of_files = []
        for file_name in os.listdir(files_path):
            list_of_files.append(files_path + file_name)
        return list_of_files

    def strip_invalid_chars(self, day_data):
        day_data = day_data.strip('\n\r')
        day_data = day_data.split(",")
        return day_data

    def read_file_data(self, file_path):
        """Reads and return file data"""
        try:
            file_reader = open(file_path, "r")
            file_data = file_reader.readlines()
            file_reader.close()
            return file_data
        except IOError:
            print("Error: can\'t find file or read data")
            exit()

    def read_files(self, files_path):
        list_of_files = self.collect_files(files_path)
        for file in list_of_files:
            file_data = self.read_file_data(file)
            for line in file_data:
                day_data = self.strip_invalid_chars(line)
                if len(day_data) > 2:
                    if day_data[0] != "PKT" and day_data[1] != "" and day_data[
                        3] != "" \
                            and day_data[8] != "":
                        self.day_weather_list.append(DayWeather(
                            day_data[0], day_data[1],
                            day_data[2], day_data[3],
                            day_data[4], day_data[5],
                            day_data[6], day_data[7],
                            day_data[8], day_data[9],
                            day_data[10], day_data[11],
                            day_data[12], day_data[13],
                            day_data[14], day_data[15],
                            day_data[16], day_data[17],
                            day_data[18], day_data[19],
                            day_data[20], day_data[21],
                            day_data[22]
                        ))

    def calc_bonus_chart(self, year_month):
        month_data_list = []
        barchart_data_list = []
        day_num = 1
        for day_data in self.day_weather_list:
            if self.check_valid_year_month_file(day_data.pkt, year_month):
                month_data_list.append(day_data)
        for day_data in month_data_list:
            barchart_min_temp = ""
            barchart_max_temp = ""
            temp_max = 0
            temp_min = 0
            if day_data.max_temperaturec != "":
                temp_max = int(day_data.max_temperaturec)
                barchart_max_temp = ColorCode.RED.value + \
                                    self.calc_barchart(temp_max)
            if day_data.min_temperaturec != "":
                temp_min = int(day_data.min_temperaturec)
                barchart_min_temp = ColorCode.BLUE.value + \
                                    self.calc_barchart(temp_min)
                barchart_data_list.append([day_num, barchart_min_temp,
                                           barchart_max_temp,
                                           temp_min, temp_max])
            day_num += 1
        return barchart_data_list

    def calc_month_chart(self, year_month):
        month_data_list = []
        barchart_data_list = []
        day_num = 1
        for day_data in self.day_weather_list:
            if self.check_valid_year_month_file(day_data.pkt, year_month):
                month_data_list.append(day_data)
        for day_data in month_data_list:
            if day_data.max_temperaturec != "":
                barchart_data_list.append([int(day_data.max_temperaturec),
                                           ColorCode.RED.value, day_num])
            if day_data.min_temperaturec != "":
                barchart_data_list.append([int(day_data.min_temperaturec),
                                           ColorCode.BLUE.value, day_num])
                day_num += 1
        return barchart_data_list

    def calc_barchart(self, temp):
        counter = 0
        barchart = ""
        while counter < temp:
            barchart += "+"
            counter += 1
        return barchart

    def extract_year_data(self, year):
        year_data_list = []
        max_data_list = []
        for day_data in self.day_weather_list:
            if self.check_valid_year_file(day_data.pkt, year):
                year_data_list.append(day_data)
        temp_max_obj = max(year_data_list,
                           key=lambda day_data: int(day_data.max_temperaturec))
        temp_min_obj = min(year_data_list,
                           key=lambda day_data: int(day_data.min_temperaturec))
        max_humid_obj = min(year_data_list,
                            key=lambda day_data: int(day_data.max_humidity))
        max_data_list.append(temp_max_obj)
        max_data_list.append(temp_min_obj)
        max_data_list.append(max_humid_obj)
        return max_data_list

    def check_valid_year_file(self, day_date, year):
        match = re.search(r'\d\d\d\d', day_date)
        if match and (year in day_date):
            return True
        else:
            return False

    def collect_average(self, month_data_list):
        avg_data_list = []
        max_temp_avg = 0
        min_temp_avg = 0
        humidity_avg = 0
        count_max_temp = 0
        count_min_temp = 0
        count_humidty = 0
        for day_data in month_data_list:
            if day_data.max_temperaturec != "":
                max_temp_avg += int(day_data.max_temperaturec)
                count_max_temp += 1
            if day_data.min_temperaturec != "":
                min_temp_avg += int(day_data.min_temperaturec)
                count_min_temp += 1
            if day_data.max_humidity != "":
                humidity_avg += int(day_data.max_humidity)
                count_humidty += 1
        avg_data_list.append(self.compute_average(max_temp_avg,
                                                  count_max_temp))
        avg_data_list.append(self.compute_average(min_temp_avg,
                                                  count_min_temp))
        avg_data_list.append(self.compute_average(humidity_avg,
                                                  count_humidty))
        return avg_data_list

    def extract_month_data(self, year_month):
        month_data_list = []
        for day_data in self.day_weather_list:
            if self.check_valid_year_month_file(day_data.pkt, year_month):
                month_data_list.append(day_data)
        return self.collect_average(month_data_list)

    def check_valid_year_month_file(self, day_date, year_month):
        match = re.search(r'\d\d\d\d', day_date)
        if match:
            day_date_list = day_date.split("-")
            year_month_list = year_month.split("/")
            if (day_date_list[0] == year_month_list[0]) and (
                    day_date_list[1] == year_month_list[1]):
                return True
            else:
                return False
        else:
            return False

    def compute_average(self, total_sum, total_elems):
        return int(total_sum / total_elems)
