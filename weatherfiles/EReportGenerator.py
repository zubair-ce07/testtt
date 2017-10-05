import sys

from datetime import datetime
from ReportGenerator import ReportGenerator


MAX_TEMP = "max_temp"
MIN_TEMP = "min_temp"
MAX_HUMIDITY = "max_humidity"


def getDate(date):
    datetime_object = datetime.strptime(date, "%Y-%m-%d")
    return (datetime_object.strftime('%B %d'))




class EReportGenerator(ReportGenerator):
    year_data = []
    recorder = {}

    def __int__(self):
        self.year_data = []

    def generate_report(self, data_list):
        for data in data_list:
            self.year_data = self.year_data + data.daily_weathers_info
        self.record_max_temp_with_date()
        self.record_min_temp_with_date()
        self.record_max_humidity_with_date()
        self.print_report()
        return


    def print_report(self):
        max_temp = self.recorder[MAX_TEMP]
        min_temp = self.recorder[MIN_TEMP]
        max_humidity = self.recorder[MAX_HUMIDITY]

        print('Highest: %dC on %s' % (max_temp[0], getDate(max_temp[1])))
        print('Lowest: %dC on %s' % (min_temp[0], getDate(min_temp[1])))
        print('Humidity: %dC on %s' % (max_humidity[0], getDate(max_humidity[1])))


        return

    def record_max(self, key, value, date):
        max = self.recorder.get(key, (0,))[0]
        if (value and value > max):
            self.recorder[key] = (value, date)

    def record_min(self, key, value, date):
        min = self.recorder.get(key, (sys.maxint,))[0]
        if (value and value < min):
            self.recorder[key] = (value, date)

    def record_max_temp_with_date(self):
        for value in self.year_data:
            self.record_max(MAX_TEMP, value.max_temp, value.date)

    def record_min_temp_with_date(self):
        for value in self.year_data:
            self.record_min(MIN_TEMP, value.min_temp, value.date)

    def record_max_humidity_with_date(self):
        for value in self.year_data:
            self.record_max(MAX_HUMIDITY, value.max_humidity, value.date)