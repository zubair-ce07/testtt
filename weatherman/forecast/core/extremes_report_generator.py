import sys

from forecast.core.extremes_report_result import ExtremesReportResult
from forecast.core.report_generator import ReportGenerator

from forecast.core.date_utils import DateUtils

MAX_TEMP = "max_temp"
MIN_TEMP = "min_temp"
MAX_HUMIDITY = "max_humidity"


class ExtremesReportGenerator(ReportGenerator):
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
        self.record_max_temp_with_date()
        self.record_min_temp_with_date()
        self.record_max_humidity_with_date()
        return self.print_report()

    def print_report(self):
        max_temp = self.recorder[MAX_TEMP]
        min_temp = self.recorder[MIN_TEMP]
        max_humidity = self.recorder[MAX_HUMIDITY]

        return ExtremesReportResult(self.year, self.month, max_temp, min_temp, max_humidity)

    def record_max(self, key, value, date):
        max = self.recorder.get(key, (0,))[0]
        if value and value > max:
            self.recorder[key] = (value, date)

    def record_min(self, key, value, date):
        min = self.recorder.get(key, (sys.maxint,))[0]
        if value and value < min:
            self.recorder[key] = (value, date)

    def record_max_temp_with_date(self):
        [self.record_max(MAX_TEMP, value.max_temp, value.date) for value in self.year_data]

    def record_min_temp_with_date(self):
        [self.record_min(MIN_TEMP, value.min_temp, value.date) for value in self.year_data]

    def record_max_humidity_with_date(self):
        [self.record_max(MAX_HUMIDITY, value.max_humidity, value.date) for value in self.year_data]
