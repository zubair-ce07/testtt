import glob
from day_weather import DayWeather
from month_weather import MonthWeather
from year_weather import YearWeather
from read_weather import ReadWeather


class WeathermanApplication:

    def __init__(self, path):
        folder = glob.glob(path+"/*.txt")

        read_weather = ReadWeather()

        self.yw = YearWeather()

        for file_path in folder:
            daily_weather = DayWeather()
            monthly_weather = MonthWeather()
            read_weather.read_weather(daily_weather, file_path)
            monthly_weather.add_month_weather(daily_weather, daily_weather.day_weather[2].pkt_dt.month)
            self.yw.add_year_weather(monthly_weather, daily_weather.day_weather[2].pkt_dt.year)
            del monthly_weather
            del monthly_weather

    def do_the_e_work(self, year_month):
        year = int(year_month)
        weather_data = self.yw.highest_temperature_day(year)
        if len(weather_data) == 2:
            print("Highest : " + str(weather_data[0]) + "C on " + weather_data[1].strftime('%b %d'))
        else:
            print(weather_data)

        weather_data = self.yw.lowest_temperature_day(year)
        if len(weather_data) == 2:
            print("Lowest : " + str(wd[0]) + "C on " + wd[1].strftime('%b %d'))
        else:
            print(weather_data)

        weather_data = self.yw.max_humidity(year)
        if len(weather_data) == 2:
            print("Humidity : " + str(weather_data[0]) + "% on " + weather_data[1].strftime('%b %d'))
        else:
            print(weather_data)

    def do_the_a_work(self, year_month):
        year_month = year_month.split('/')
        weather_data = self.yw.average_highest_temperature(int(year_month[0]), int(year_month[1]))
        print("Highest Average : " + str(round(weather_data, 2)) + "C")

        weather_data = self.yw.average_lowest_temperature(int(year_month[0]), int(year_month[1]))
        print("Lowest Average : " + str(round(weather_data, 2)) + "C")

        weather_data = self.yw.average_mean_humidity(int(year_month[0]), int(year_month[1]))
        print("Average Mean Humidity : " + str(round(weather_data, 2)) + "%")

    def do_the_c_work(self, year_month):
        year_month = year_month.split('/')
        self.yw.print_bar_chart(int(year_month[0]), int(year_month[1]))

    def do_the_c_work2(self, year_month):
        year_month = year_month.split('/')
        self.yw.print_bar_chart2(int(year_month[0]), int(year_month[1]))

    def testing(self, year_month):
        year_month = year_month.split('/')
        print(self.yw.year_weather[int(year_month[0])][int(year_month[1])].month_weather)

    def do_the_dew(self, argv):

        count = 1
        while count < len(argv):
            option = argv[count]
            count = count + 1
            year_month = argv[count]
            count = count + 1
            if option == "-e":
                self.do_the_e_work(year_month)
            elif option == "-a":
                self.do_the_a_work(year_month)
            elif option == "-c":
                self.do_the_c_work(year_month)
            else:
                print("Function is not recognized.")
            print()
