from math import inf
import calendar


class WeathermanClass:
    def max_temp_min_temp_max_humidity(self, weather_data):
        max_temp_date = ""
        max_temp = -inf
        min_temp_date = ""
        min_temp = +inf
        max_humidity_date = ""
        max_humidity = -inf
        for data in weather_data[0]:
            data = dict(data)
            if data["Max TemperatureC"]:
                if max_temp <= int(data["Max TemperatureC"]):
                    max_temp_date = data["PKT"]
                    max_temp = int(data["Max TemperatureC"])
            if data["Min TemperatureC"]:
                if min_temp >= int(data["Min TemperatureC"]):
                    min_temp_date = data["PKT"]
                    min_temp = int(data["Min TemperatureC"])
            if data["Max Humidity"]:
                if max_humidity <= int(data["Max Humidity"]):
                    max_humidity_date = data["PKT"]
                    max_humidity = int(data["Max Humidity"])
        print("Highest: " + str(max_temp) + "C " +
              "on " + str(self.date_format(max_temp_date)))
        print("Lowest: " + str(min_temp) + "C " + "on " +
              str(self.date_format(min_temp_date)))
        print("Humidity: " + str(max_humidity) + "% " +
              "on " + str(self.date_format(max_humidity_date)))

    def date_format(self, date):
        split_date = date.split("-")
        return calendar.month_name[int(split_date[1])] + " " + split_date[2]

    def average_max_min_temp_mean_himidity(self, weather_dict):
        sum_max_temp = 0
        max_temp_count = 0
        sum_min_temp = 0
        min_temp_count = 0
        sum_mean_humidity = 0
        mean_humidity_count = 0
        for data in weather_dict[0]:
            data = dict(data)
            if data["Max TemperatureC"]:
                sum_max_temp += int(data["Max TemperatureC"])
                max_temp_count += 1
            if data["Min TemperatureC"]:
                sum_min_temp += int(data["Min TemperatureC"])
                min_temp_count += 1
            if data[" Mean Humidity"]:
                sum_mean_humidity += int(data[" Mean Humidity"])
                mean_humidity_count += 1
        avg_max_temp = sum_max_temp // max_temp_count
        avg_min_temp = sum_min_temp // min_temp_count
        avg_mean_humidity = (
            sum_mean_humidity // mean_humidity_count)
        print("Highest Average: " + str(avg_max_temp) + "C")
        print("Lowest Average: " + str(avg_min_temp) + "C")
        print("Average Mean Humidity: " + str(avg_mean_humidity) + "%")

    def each_day_bar(self, weather_dict, key):
        max_temp = 0
        min_temp = 0
        date = ''
        for data in weather_dict[0]:
            data = dict(data)
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
