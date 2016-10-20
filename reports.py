from colors import Colors as col
import common as wc
import constants as const

from os import listdir


class ReportGenerator:

    def __init__(self, path, **kwargs):
        self.path = path
        self.data_files = set(listdir(path))

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

        hi = -274
        hi_day = ""

        lo = -274
        lo_day = ""

        humidity = -1
        humid_day = ""

        for file_name in self.data_files:
            if year in file_name:
                file_path = self.path + "/" + file_name
                content = open(file_path).readlines()
                for line in content[1:]:
                    data_points = line.split(',')

                    data = data_points[const.HI_TEMP]
                    if data != "" and int(data) > hi:
                        hi = int(data)
                        hi_day = wc.get_day(data_points[0])

                    data = data_points[const.LO_TEMP]
                    if data != "" and (lo == -274 or int(lo) < lo):
                        lo = int(data)
                        lo_day = wc.get_day(data_points[0])

                    data = data_points[const.HUMID]
                    if data != "" and (humidity < 0 or int(data) > humidity):
                        humidity = int(data)
                        humid_day = wc.get_day(data_points[0])

        print "Highest: " + str(hi) + "C on " + hi_day
        print "Lowest: " + str(lo) + "C on " + lo_day
        print "Humidity: " + str(humidity) + "% on " + humid_day

    def get_monthly_avgs(self, month):
        file_name = "Murree_weather_%s.txt" % month

        if file_name in self.data_files:
            file_path = self.path + "/" + file_name
            content = open(file_path).readlines()

            if len(content) < 2:
                raise Exception("No data points recorded for the month (%s)"
                                % month)

            # Initialize datapoints
            data_points = content[1].split(',')
            avg_hi_temp = int(data_points[const.HI_TEMP])
            avg_lo_temp = int(data_points[const.LO_TEMP])
            avg_humidity = int(data_points[const.HUMID])
            hi_count = 1
            lo_count = 1
            humid_count = 1

            for line in content[2:]:
                data_points = line.split(',')

                # Update moving average for Hi
                # temperate data points
                data = data_points[const.HI_TEMP]
                if data != "":
                    data = int(data)
                    hi_count = hi_count + 1
                    avg_hi_temp = avg_hi_temp + \
                        (data - avg_hi_temp)/hi_count

                # Updat moving average for Lo
                # temperature data points
                data = data_points[const.LO_TEMP]
                if data != "":
                    data = int(data)
                    lo_count = lo_count + 1
                    avg_lo_temp = avg_lo_temp + \
                        (data - avg_lo_temp)/lo_count

                # Updat moving average for
                # Humidity data points
                data = data_points[const.HUMID]
                if data != "":
                    data = int(data)
                    humid_count = humid_count + 1
                    avg_humidity = avg_humidity + \
                        (data - avg_humidity)/humid_count

            print "Highest Averaeg: " + str(avg_hi_temp) + "C"
            print "Lowest Average: " + str(avg_lo_temp) + "C"
            print "Average Mean Humidity: " + str(avg_humidity) + "%"

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
