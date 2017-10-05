import sys

from Colors import Colors
from ReportGenerator import ReportGenerator

MAX_AVG_TEMP = "max_avg_temp"
MIN_AVG_TEMP = "min_avg_temp"
MAX_AVG_HUMIDITY = "max_avg_humidity"


class CReportGenerator(ReportGenerator):
    year_data = []
    recorder = {}

    def __int__(self):
        self.year_data = []
        self.recorder = {}

    def generate_report(self, data_list):
        if len(data_list) == 0:
            print(Colors.RED + "No data recorded for this time period" + Colors.RESET)
            sys.exit(0)

        for data in data_list:
            self.year_data = self.year_data + data.daily_weathers_info
        self.print_report()

    def print_report(self):
        for data in self.year_data:
            self.print_max(data)
            self.print_min(data)

    @staticmethod
    def print_max(data):
        try:
            print(data.get_day_as_string() + " | " + Colors.RED + ("+" * data.max_temp)
                  + Colors.RESET + " " + str(data.max_temp) + "C")
        except TypeError:
            print(data.get_day_as_string() + Colors.YELLOW + " | No Data" + Colors.RESET)

    @staticmethod
    def print_min(data):
        try:
            print(data.get_day_as_string() + " | " + Colors.BLUE + ("+" * data.min_temp)
                  + Colors.RESET + " " + str(data.min_temp) + "C")
        except TypeError:
            print(data.get_day_as_string() + Colors.YELLOW + " | No Data" + Colors.RESET)