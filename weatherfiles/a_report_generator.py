import sys

from report_generator import ReportGenerator

MAX_AVG_TEMP = "max_avg_temp"
MIN_AVG_TEMP = "min_avg_temp"
MAX_AVG_HUMIDITY = "max_avg_humidity"


class AReportGenerator(ReportGenerator):
    year_data = []
    recorder = {}

    def __int__(self):
        self.year_data = []
        self.recorder = {}

    def generate_report(self, data_list):
        if len(data_list) == 0:
            print("No data recorded for this time period")
            sys.exit(0)

        for data in data_list:
            self.year_data = self.year_data + data.daily_weathers_info
        self.record_average_max_temp()
        self.record_average_min_temp()
        self.record_average_mean_humidity()
        self.print_report()

    def print_report(self):
        max_temp = self.recorder[MAX_AVG_TEMP]
        min_temp = self.recorder[MIN_AVG_TEMP]
        max_humidity = self.recorder[MAX_AVG_HUMIDITY]

        print('Highest Average: %dC' % (max_temp))
        print('Lowest Average: %dC' % (min_temp))
        print('Average Mean Humidity: %d%%' % (max_humidity))

    def record_average_max_temp(self):
        max_counter = 0
        non_null_value_counter = 0
        for value in self.year_data:
            if value.max_temp:
                max_counter += value.max_temp
                non_null_value_counter += 1
        self.recorder[MAX_AVG_TEMP] = max_counter / non_null_value_counter

    def record_average_min_temp(self):
        min_counter = 0
        non_null_value_counter = 0
        for value in self.year_data:
            if value.max_temp:
                min_counter += value.min_temp
                non_null_value_counter += 1
        self.recorder[MIN_AVG_TEMP] = min_counter / non_null_value_counter

    def record_average_mean_humidity(self):
        min_counter = 0
        non_null_value_counter = 0
        for value in self.year_data:
            if value.mean_humidity:
                min_counter += value.mean_humidity
                non_null_value_counter += 1
        self.recorder[MAX_AVG_HUMIDITY] = min_counter / non_null_value_counter
