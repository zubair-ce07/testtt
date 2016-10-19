import legend as leg
from colors import Colors as col

from os import listdir


# This is an ordered list please do not change order of elements
MONTHS=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', \
        'Nov', 'Dec']


class ReportGenerator:

    def __init__(self, path, **kwargs):
        self.path = path
        self.data_files = set(listdir(path))
        self.exts = kwargs.pop("exts", [])
        self.avgs = kwargs.pop("avgs", [])
        self.charts = kwargs.pop("charts", [])

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

                    data = data_points[leg.HI_TEMP]
                    if data != "" and int(data) > hi:
                        hi = int(data)
                        hi_day = self.get_day(data_points[0])

                    data = data_points[leg.LO_TEMP]
                    if data != "" and (lo == -274 or int(lo) < lo):
                        lo = int(data)
                        lo_day = self.get_day(data_points[0])

                    data = data_points[leg.HUMID]
                    if data != "" and (humidity < 0 or int(data) > humidity):
                        humidity = int(data)
                        humid_day = self.get_day(data_points[0])

        print "Highest: " + str(hi) + "C on " + hi_day
        print "Lowest: " + str(lo) + "C on " + lo_day
        print "Humidity: " + str(humidity) + "% on " + humid_day


    def get_day(self, date):
        date = date.split("-")
        month = MONTHS[int(date[1]) - 1]
        return month + " " + date[2]

    def get_monthly_avgs(self, month):
        file_name = "Murree_weather_%s.txt" % month

        if file_name in self.data_files:
            file_path = self.path + "/" + file_name
            raw_input(file_path)
            content = open(file_path).readlines()
            
            if len(content) < 2:
                raise Exception("No data points recorded for the month (%s)" \
                                % month)

            # Initialize datapoints
            data_points = content[1].split(',')
            avg_hi_temp = data_points[leg.HI_TEMP]
            avg_lo_temp = data_points[leg.LO_TEMP]
            avg_humidity = data_points[leg.HUMID]
            hi_count = 1
            lo_count = 1
            humid_count = 1

            for line in content[2:]:
                data_points = line.split(',')

                # Update moving average for Hi
                # temperate data points
                data = data_points[leg.HI_TEMP]
                if data != "":
                    data = int(data)
                    hi_count = hi_count + 1
                    avg_hi_temp = avg_hi_temp + \
                                  (data - avg_hi_temp)/hi_count

                # Updat moving average for Lo
                # temperature data points
                data = data_points[leg.LO_TEMP]
                if data != "":
                    data = int(data)
                    lo_count = lo_count + 1
                    avg_lo_temp = avg_lo_temp + \
                                  (data - avg_lo_temp)/lo_count

                # Updat moving average for
                # Humidity data points
                data = data_points[leg.HUMID]
                if data != "":
                    data = int(data)
                    humid_count = humid_count + 1
                    avg_humidity = avg_humidity + \
                                   (data - avg_humidity)/humid_count

            print "Highest Averaeg: " + avg_hi_temp + "C"
            print "Lowest Average: " + avg_lo_temp + "C"
            print "Average Mean Humidity: " + avg_humidity + "%"

    def draw_charts(self, month):

        file_name = "Murree_weather_%s.txt" % month

        if file_name in self.data_files:
            file_path = self.path + "/" + file_name
            content = open(file_path).readlines()

            if len(content) < 2:
                raise Exception("No data points recorded for the month (%s)" \
                                 % month)
            
            for line in content[1:]:
                data_points = line.split(',')
                date = data_points[leg.DATE]
                day = date.split('-')[2]
                hi_temp = data_points[leg.HI_TEMP]
                lo_temp = data_points[leg.LO_TEMP]

                hi_bar = col.RED + ""
                lo_bar = col.BLUE + ""

                if hi_temp != "":
                    hi_bar = hi_bar + ("+" * int(hi_temp)) + col.ENDC
                    hi_temp = hi_temp + "C"

                if lo_temp != "":
                    lo_bar = lo_bar + ("+" * int(lo_temp)) + col.ENDC
                    lo_temp = lo_temp + "C"

                lo_bar = lo_bar + col.ENDC
                hi_bar = hi_bar + col.ENDC

                print day + " " + lo_bar + hi_bar + " " + lo_temp + " - " \
                      + hi_temp
