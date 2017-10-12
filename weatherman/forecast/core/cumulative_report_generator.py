import sys

from forecast.core.colors import Colors
from forecast.core.cumulative_report_result import CumulativeReportResult

from forecast.core.report_generator import ReportGenerator

MAX_AVG_TEMP = "max_avg_temp"
MIN_AVG_TEMP = "min_avg_temp"
MAX_AVG_HUMIDITY = "max_avg_humidity"


class CumulativeReportGenerator(ReportGenerator):
    year_data = []
    recorder = {}

    def __init__(self):
        self.year_data = []
        self.recorder = {}
        self.month = ''
        self.year = ''

    def generate_report(self, data_list, year, month):
        if not data_list:
            print(Colors.RED + "No data recorded for this time period" + Colors.RESET)
            return

        self.month = month
        self.year = year

        self.year_data = data_list
        return self.print_report()

    def print_report(self):
        month_data = self.year_data[0]
        return CumulativeReportResult(self.year, self.month, month_data.daily_weathers_info)