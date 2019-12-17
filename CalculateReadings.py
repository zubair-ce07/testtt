from Parser import *
from ReportDisplay import *
import os


class CalculateReadings:

    def __init__(self, file_name):
        self.parser = Parser(file_name)
        self.results = Results()

    def cal_highest_average_monthly(self):
        for row in self.parser.weather_reading.rows:
            self.results.average_highest_temperature += row[1]

        self.results.average_highest_temperature\
            /= len(self.parser.weather_reading.rows)

        return self.results.average_highest_temperature

    def cal_lowest_average_monthly(self):
        for row in self.parser.weather_reading.rows:
            self.results.average_lowest_temperature += row[3]

        self.results.average_lowest_temperature \
            /= len(self.parser.weather_reading.rows)

        return self.results.average_lowest_temperature

    def cal_average_mean_humidity_monthly(self):
        for row in self.parser.weather_reading.rows:
            self.results.average_humidity += row[8]

        self.results.average_humidity \
            /= len(self.parser.weather_reading.rows)

        return self.results.average_humidity

    def cal_report_A(self):
        self.cal_highest_average_monthly()
        self.cal_lowest_average_monthly()
        self.cal_average_mean_humidity_monthly()

    def set_highest_lowest_temperature_monthly(self):
        for index in range(len(self.parser.weather_reading.rows)):
            self.results.highest_temperature_monthly.\
                append(self.parser.weather_reading.rows[index][1])
            self.results.lowest_temperature_monthly.\
                append(self.parser.weather_reading.rows[index][3])

    def cal_report_C(self):
        self.set_highest_lowest_temperature_monthly()

    def set_highest_temperature(self):
        self.results.highest_temperature = max(
            elem[1] for elem in self.parser.weather_reading.rows)
        return self.results.highest_temperature

    def set_lowest_temperature(self):
        self.results.lowest_temperature = min(
            elem[3] for elem in self.parser.weather_reading.rows)
        return self.results.lowest_temperature

    def set_highest_humidity(self):
        self.results.highest_humidity = max(
            elem[7] for elem in self.parser.weather_reading.rows)
        return self.results.highest_humidity
