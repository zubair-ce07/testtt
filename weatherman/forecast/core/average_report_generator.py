import sys

from forecast.core.average_report_result import AverageReportResult
from forecast.core.report_generator import ReportGenerator

MAX_AVG_TEMP = "max_avg_temp"
MIN_AVG_TEMP = "min_avg_temp"
MAX_AVG_HUMIDITY = "max_avg_humidity"


class AverageReportGenerator(ReportGenerator):
    year_data = []
    recorder = {}

    def __init__(self):
        self.year_data = []
        self.recorder = {}
        self.month = ''
        self.year = ''

    def generate_report(self, data_list, year, month):
        if not data_list:
            print("No data recorded for this time period")
            return

        self.month = month
        self.year = year

        for data in data_list:
            self.year_data = self.year_data + data.daily_weathers_info

        self.record_average_max_temp()
        self.record_average_min_temp()
        self.record_average_mean_humidity()
        return self.print_report()

    def print_report(self):
        max_temp = self.recorder[MAX_AVG_TEMP]
        min_temp = self.recorder[MIN_AVG_TEMP]
        humidity = self.recorder[MAX_AVG_HUMIDITY]

        return AverageReportResult(self.year, self.month, max_temp, min_temp, humidity)

    def record_average_max_temp(self):
        max_temp_list = [value.max_temp for value in self.year_data]
        self.recorder[MAX_AVG_TEMP] = AverageReportGenerator.average(max_temp_list)

    def record_average_min_temp(self):
        min_temp_list = [value.min_temp for value in self.year_data]
        self.recorder[MIN_AVG_TEMP] = AverageReportGenerator.average(min_temp_list)

    def record_average_mean_humidity(self):
        min_humidity_list = [value.mean_humidity for value in self.year_data]
        self.recorder[MAX_AVG_HUMIDITY] = AverageReportGenerator.average(min_humidity_list)

    @staticmethod
    def average(list):
        value_counter = 0
        non_null_value_counter = 0
        for value in list:
            if value is not None:
                value_counter += value
                non_null_value_counter += 1
        return value_counter / non_null_value_counter
