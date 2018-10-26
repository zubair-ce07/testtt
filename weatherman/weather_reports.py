import calendar

from calculations import Calculations
from file_reading import file_reading


class WeatherReports:
    def extreme_weather(self, dir_path, year, month):
        weather_data = file_reading(dir_path, year, month)

        if weather_data:
            calculate = Calculations()
            extreme_weather = calculate.calculate_extreme_weather(weather_data)
            print(f"---------------Weather Report of {year}-----------------")
            print(f"Highest: {str(extreme_weather['max_temp'])} C on "
                  f"{self.date_format(extreme_weather['max_temp_date'])}")
            print(f"Lowest: {str(extreme_weather['min_temp'])} C on "
                  f"{self.date_format(extreme_weather['min_temp_date'])}")
            print(f"Humidity: {str(extreme_weather['max_humidity'])} % on "
                  f"{self.date_format(extreme_weather['max_humidity_date'])}")

    def date_format(self, date):
        split_date = date.split("-")
        return calendar.month_name[int(split_date[1])] + " " + split_date[2]

    def average_weather(self, dir_path, year, month):
        weather_data = file_reading(dir_path, year, month)

        if weather_data:
            calculate = Calculations()
            average_weather = calculate.calculate_average_weather(weather_data)
            print(f"----------------Weather Report of {year}---------------------")
            print(f"Highest Average: {str(average_weather['avg_max_temp'])} C")
            print(f"Lowest Average: {str(average_weather['avg_min_temp'])} C")
            print(f"Average Mean Humidity: {str(average_weather['avg_mean_humidity'])} %")

    def weather_charts(self, dir_path, year, month, key):
        weather_data = file_reading(dir_path, year, month)

        if weather_data:
            print(f"----------------Weather Report of {year}---------------------")
            for data in weather_data:

                if (data["Max TemperatureC"] and
                        data["Min TemperatureC"]):
                    max_temp = int(data["Max TemperatureC"])
                    min_temp = int(data["Min TemperatureC"])
                    date = str(data["PKT"]).split("-")[2]

                    if len(date) == 1:
                        date = "0" + date

                    if key is 'c':
                        print("\33[95m" + date, end=" ")
                        print("\33[31m" + "+" * max_temp, end=" ")
                        print("\33[95m" + str(max_temp) + "C")
                        print("\33[95m" + date, end=" ")
                        print("\33[94m" + "+" * min_temp, end=" ")
                        print("\33[95m" + str(min_temp) + "C" + "\33[0m")

                    elif key is 'cb':
                        print("\33[95m" + date, end=" ")
                        print("\33[94m" + "+" * min_temp, end="")
                        print("\33[31m" + "+" * max_temp, end=" ")
                        print("\33[95m" + str(min_temp) + "C", end=" - ")
                        print("\33[95m" + str(max_temp) + "C" + "\33[0m")
