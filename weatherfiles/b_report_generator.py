import sys

from colors import Colors
from report_generator import ReportGenerator

MAX_AVG_TEMP = "max_avg_temp"
MIN_AVG_TEMP = "min_avg_temp"
MAX_AVG_HUMIDITY = "max_avg_humidity"


class BReportGenerator(ReportGenerator):
    year_data = []
    recorder = {}

    def __int__(self):
        self.year_data = []
        self.recorder = {}

    def generate_report(self, data_list):
        if len(data_list) == 0:
            print(Colors.RED + "No data recorded for this time period" + Colors.RESET)
            sys.exit(0)

        self.year_data = data_list
        self.print_report()

    def print_report(self):
        for month_data in self.year_data:
            print(month_data.get_display_month())
            for data in month_data.daily_weathers_info:
                self.print_min_max(data)

    @staticmethod
    def print_min_max(data):
        try:
            print(data.get_day_as_string() + " | " + Colors.RED + ("+" * data.max_temp)
                  + Colors.BLUE + ("+" * data.min_temp)
                  + Colors.RESET + " " + str(data.min_temp) + "C"
                  + " - " + str(data.max_temp) + "C")
        except TypeError:
            print(data.get_day_as_string() + Colors.YELLOW + " | No Data" + Colors.RESET)
