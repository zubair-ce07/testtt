import glob
from DayWeather import DayWeather
from Monthweather import MonthWeather
from YearWeather import YearWeather
from ReadWeather import ReadWeather


class WeathermanApplication:

    def __init__(self):
        folder = glob.glob("./weatherfiles/*.txt")

        rw = ReadWeather()

        self.yw = YearWeather()

        for fp in folder:
            dw = DayWeather()
            mw = MonthWeather()
            rw.read_weather(dw, fp)
            mw.add_month_weather(dw, dw.day_weather[2].pkt_dt.month)
            self.yw.add_year_weather(mw, dw.day_weather[2].pkt_dt.year)
            del dw
            del mw

    def do_the_e_work(self, y_m):
        year = int(y_m)
        wd = self.yw.highest_temperature_day(year)
        if len(wd) == 2:
            print("Highest : " + str(wd[0]) + "C on " + wd[1].strftime('%b %d'))
        else:
            print(wd)

        wd = self.yw.lowest_temperature_day(year)
        if len(wd) == 2:
            print("Lowest : " + str(wd[0]) + "C on " + wd[1].strftime('%b %d'))
        else:
            print(wd)

        wd = self.yw.max_humidity(year)
        if len(wd) == 2:
            print("Humidity : " + str(wd[0]) + "% on " + wd[1].strftime('%b %d'))
        else:
            print(wd)

    def do_the_a_work(self, y_m):
        year_month = y_m.split('/')
        wd = self.yw.average_highest_temperature(int(year_month[0]), int(year_month[1]))
        print("Highest Average : " + str(round(wd, 2)) + "C")

        wd = self.yw.average_lowest_temperature(int(year_month[0]), int(year_month[1]))
        print("Lowest Average : " + str(round(wd, 2)) + "C")

        wd = self.yw.average_mean_humidity(int(year_month[0]), int(year_month[1]))
        print("Average Mean Humidity : " + str(round(wd, 2)) + "%")

    def do_the_c_work(self, y_m):
        year_month = y_m.split('/')
        self.yw.print_bar_chart(int(year_month[0]), int(year_month[1]))

    def do_the_c_work2(self, y_m):
        year_month = y_m.split('/')
        self.yw.print_bar_chart2(int(year_month[0]), int(year_month[1]))

    def testing(self, y_m):
        year_month = y_m.split('/')
        print(self.yw.year_weather[int(year_month[0])][int(year_month[1])].month_weather)


    def do_the_dew(self, arglist):

        count = 1
        while count < len(arglist):
            option = arglist[count]
            count = count + 1
            y_m = arglist[count]
            count = count + 1
            if option == "-e":
                self.do_the_e_work(y_m)
            elif option == "-a":
                self.do_the_a_work(y_m)
            elif option == "-c":
                self.do_the_c_work(y_m)
            else:
                self.testing(y_m)
            print()
