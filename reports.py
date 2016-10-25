from colors import Colors as col
import common as wc
import constants as const
import csv 
from datetime import datetime

from os import listdir
from os import path


class ReportGenerator:

    def __init__(self, path, **kwargs):
        self.path = path
        self.data_files = set(listdir(path))

        self.max_temp = -274
        self.max_temp_day = ""
        self.min_temp = -274
        self.min_temp_day = ""
        self.max_humidity = -1
        self.max_humid_day = ""

    def yearly_extremes_bulk(self, years):
        for year in years:
            self.yearly_extremes(year)

    def monthly_avgs_bulk(self, months):
        for month in months:
            self.monthly_avgs(month)

    def draw_charts_bulk(self, months):
        for month in months:
            self.draw_charts(month)

    def yearly_extremes(self, year):
        for file_name in self.data_files:
            if year in file_name:
                file_path = path.join(self.path, file_name)
                with open(file_path) as f:
                    content = csv.DictReader(f) 
                    for row in content:
                        self.update_extremes(row)
        self.print_extremes()

    def update_extremes(self, row):
        max_temp, min_temp, max_humidity, _ = self.get_data(row)

        if max_temp and max_temp > self.max_temp:
            self.max_temp = max_temp
            self.max_temp_day = wc.get_month_day(row)

        if min_temp and (self.min_temp == -274 or min_temp < self.min_temp):
            self.min_temp = min_temp
            self.min_temp_day = wc.get_month_day(row)

        if max_humidity and (self.max_humidity < 0 or max_humidity
                           > self.max_humidity):
            self.max_humidity = max_humidity
            self.max_humid_day = wc.get_month_day(row)

    def print_extremes(self):
        print "Highest: " + str(self.max_temp) \
              + "C on " + self.max_temp_day
        print "Lowest: " + str(self.min_temp) + "C on " \
              + self.min_temp_day
        print "Humidity: " + str(self.max_humidity) + "% on " \
              + self.max_humid_day

    def monthly_avgs(self, month):
        max_temps = []
        min_temps = []
        avg_humids = []

        for file_name in self.data_files:
            if month in file_name:
                file_path = path.join(self.path, file_name)
                with open(file_path) as f:
                    content = csv.DictReader(f)

                    for row in content:
                        max_temp, min_temp, _, avg_humidity \
                            = self.get_data(row)

                        if max_temp:
                            max_temps.append(max_temp)

                        if min_temp:
                            min_temps.append(min_temp)

                        if avg_humidity:
                            avg_humids.append(avg_humidity)

        avg_max_temp, avg_min_temp, avg_humidity = self.get_monthly_avgs(
                                                       max_temps,
                                                       min_temps,
                                                       avg_humids)
        self.print_monthly_avgs(avg_max_temp, avg_min_temp, avg_humidity)

    def get_data(self, row):
        max_temp, min_temp, max_humidity, avg_humidity = (row[const.HI_TEMP],
                                                          row[const.LO_TEMP],
                                                          row[const.HI_HUMID],
                                                          row[const.AVG_HUMID])
        if max_temp:
            max_temp = int(max_temp)

        if min_temp:
            min_temp = int(min_temp)

        if max_humidity:
            max_humidity = int(max_humidity)

        if avg_humidity:
            avg_humidity = int(avg_humidity)

        return (max_temp, min_temp, max_humidity, avg_humidity)

    def get_monthly_avgs(self, max_temps, min_temps, avg_humids):
        max_temp_avg = sum(max_temps)/len(max_temps)
        min_temp_avg = sum(min_temps)/len(min_temps)
        avg_humid = sum(avg_humids)/len(avg_humids)

        return (max_temp_avg, min_temp_avg, avg_humid)

    def print_monthly_avgs(self, avg_max_temp, avg_min_temp, avg_humid):
        print "Highest Averaeg: " + str(avg_max_temp) + "C"
        print "Lowest Average: " + str(avg_min_temp) + "C"
        print "Average Mean Humidity: " + str(avg_humid) + "%"

    def draw_charts(self, month):
        file_name = "Murree_weather_%s.txt" % month

        if file_name in self.data_files:
            file_path = self.path + "/" + file_name
            f = open(file_path).readlines()
            content = csv.DictReader(f)

            for data_points in content:
                date = datetime.strptime(data_points[const.DATE],
                                         const.DATE_FORMAT)
                hi_temp = data_points[const.HI_TEMP]
                lo_temp = data_points[const.LO_TEMP]

                hi_bar = col.RED + ""
                lo_bar = col.BLUE + ""

                if hi_temp != "":
                    hi_bar = hi_bar + ("+" * abs(int(hi_temp))) + col.ENDC
                    hi_temp = hi_temp + "C"

                if lo_temp != "":
                    lo_bar = lo_bar + ("+" * abs(int(lo_temp))) + col.ENDC
                    lo_temp = lo_temp + "C"

                lo_bar = lo_bar + col.ENDC
                hi_bar = hi_bar + col.ENDC

                print str(date.day) + " " + lo_bar + hi_bar + " " + lo_temp + \
                      " - " + hi_temp
