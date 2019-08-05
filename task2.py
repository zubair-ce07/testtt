import copy
import csv
import sys
import os
from read_file import read_file
from data import data


class task2(data):
    def average_highest_temperature_cal(self,highest_temperature,highest_temperature_count):
        return highest_temperature/highest_temperature_count

    def average_lowest_temperature_cal(self,lowest_temperature, lowest_temperature_count):
        return lowest_temperature/lowest_temperature_count

    def average_mean_humidity_cal(self,mean_humidity,mean_humidity_count):
        return mean_humidity/mean_humidity_count

    def task(self, month, year):
        read_file.read_months(self.month_check[month],
                            year, self.list_month, self.list_year, self.dic, self.day)

        average_highest_temperature = None
        highest_temperature = 0
        highest_temperature_count = 0

        average_lowest_temperature = None
        lowest_temperature = 0
        lowest_temperature_count = 0

        average_mean_humidity = None
        mean_humidity = 0
        mean_humidity_count = 0

        for count in range(len(self.list_year)):
            if self.list_year[count] is not None:
                for data in self.list_year[count]:
                    if data["Max TemperatureC"] != '':
                        highest_temperature += int(data["Max TemperatureC"])
                        highest_temperature_count += 1
                    if data["Min TemperatureC"] != '':
                        lowest_temperature = int(data["Min TemperatureC"])
                        lowest_temperature_count += 1
                    if data["Mean Humidity"] != '':
                        mean_humidity = int(data["Mean Humidity"])
                        mean_humidity_count += 1

        print("Average highest temperature in " + self.month_check[month] +
              " is: ", self.average_highest_temperature_cal(highest_temperature,highest_temperature_count))
        print("Average lowest temperature in " + self.month_check[month] +
              " is: ", self.average_lowest_temperature_cal(lowest_temperature, lowest_temperature_count))
        print("Average mean humidity in " +
              self.month_check[month] + " is: ",self. average_mean_humidity_cal(mean_humidity,mean_humidity_count))


