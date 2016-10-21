from colors import Colors as col
import common as wc
import constants as const
import csv 

from os import listdir


class ReportGenerator:

    def __init__(self, path, **kwargs):
        self.path = path
        self.data_files = set(listdir(path))

        self.hi = -274
        self.hi_day = ""
        self.lo = -274
        self.lo_day = ""
        self.humidity = -1
        self.humid_day = ""

    def get_yearly_extremes_bulk(self, years):
        for year in years:
            self.get_yearly_extremes(year)

    def get_monthly_avgs_bulk(self, months):
        for month in months:
            self.get_monthly_avgs(month)

    def draw_charts_bulk(self, months):
        for month in months:
            self.draw_charts(month)

    def get_yearly_extremes(self, year):
        for file_name in self.data_files:
            if year in file_name:
                file_path = self.path + "/" + file_name
                f = open(file_path)
                content = cvs.DictReader(f) 
                for line in content:
                    self.process_exctremes(line)

    def process_extremes(self, data_points):
        data = data_points[const.HI_TEMP]
        if data != "" and int(data) > self.hi:
            self.hi = int(data)
            self.hi_day = wc.get_day(data_points[0])

        data = data_points[const.LO_TEMP]
        if data != "" and (lo == -274 or int(data) < self.lo):
            self.lo = int(data)
            self.lo_day = wc.get_day(data_points[0])

        data = data_points[const.HI_HUMID]
        if data != "" and (self.humidity < 0 or int(data)
                           > self.humidity):
            self.humidity = int(data)
            self.humid_day = wc.get_day(data_points[0])

    def print_extremes(self):
        print "Highest: " + str(self.hi) + "C on " + self.hi_day
        print "Lowest: " + str(self.lo) + "C on " + self.lo_day
        print "Humidity: " + str(self.humidity) + "% on " + self.humid_day

    def get_monthly_avgs(self, month):
        file_name = "Murree_weather_%s.txt" % month

        if file_name in self.data_files:
            file_path = self.path + "/" + file_name
            f = open(file_path)
            content = cvs.DictReader(f)

            if len(content) < 2:
                raise Exception("No data points recorded for the month (%s)"
                                % month)

            self.process_monthly_avgs(content)

    def process_monthly_avgs(self, content):
        hi_temps = []
        lo_temps = []
        avg_humids = []

        for line in content:
            data = data_points[const.HI_TEMP]
            if data != "":
                hi_temps.append(int(data))

            data = data_points[const.LO_TEMP]
            if data != "":
                lo_temps.append(int(data))

            data = data_points[const.HUMID]
            if data != "":
                avg_humids.append(int(data))

    def print_monthly_avgs(self, avg_hi_temp, avg_lo_temp, avg_humid)
            print "Highest Averaeg: " + str(avg_hi_temp) + "C"
            print "Lowest Average: " + str(avg_lo_temp) + "C"
            print "Average Mean Humidity: " + str(avg_humid) + "%"

    def draw_charts(self, month):

        file_name = "Murree_weather_%s.txt" % month

        if file_name in self.data_files:
            file_path = self.path + "/" + file_name
            content = open(file_path).readlines()

            if len(content) < 2:
                raise Exception("No data points recorded for the month (%s)"
                                % month)

            for line in content[1:]:
                data_points = line.split(',')
                date = data_points[const.DATE]
                day = date.split('-')[2]
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

                print day + " " + lo_bar + hi_bar + " " + lo_temp + " - " \
                    + hi_temp
