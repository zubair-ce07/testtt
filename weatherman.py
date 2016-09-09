import os
import csv
import sys
import calendar


def skip_last_line(it):
    prev = next(it)
    for item in it:
        yield prev
        prev = item


class Weather:
    __dated_weather_data = []
    # date, maxTemp, minTemp, maxHumid
    __month = ""
    __year = ""
    __specified_month_temp = []
    # day, maxT, minT
    __monthly_avg_temp = []
    # year, month, avg_maxT, avg_minT, avg_maxH
    __yearly_max_temp = []
    # year, month, day, maxTemp
    __yearly_min_temp = []
    # year, month, day, minTemp
    __yearly_max_humidity = []
    # year, month, day, maxHumidity

    def __init__(self, path_to_dir, _year="", _month=""):
        self.__year = _year
        self.__month = _month
        Weather.read_data(self, path_to_dir)
        Weather.process_data(self, _year, _month)

    def read_data(self, path_to_dir):
        for root, dirs, files in os.walk(path_to_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path) as file:
                    if file.closed:
                        print("unable to read from:", file_name)
                        continue
                    else:
                        next(file)
                        csv_file = csv.DictReader(file)
                        for line in skip_last_line(csv_file):
                            if not line["Min TemperatureC"] or \
                                            not line["Max TemperatureC"] or \
                                            not line["Max Humidity"]:
                                # Do not read this particular day if its -
                                # - missing values of Min or Max temp or humidity
                                continue
                            self.__dated_weather_data.append((str(line.get("PKT") or
                                                                  line.get("PKST")),
                                                              int(line.get("Max TemperatureC")),
                                                              int(line.get("Min TemperatureC")),
                                                              int(line.get("Max Humidity"))))

    def process_data(self, _year, _month):
        days_in_month = 0
        max_temp_sum = 0
        min_temp_sum = 0
        humidity_sum = 0
        highest_temp = 0
        highest_temp_date = ""
        lowest_temp = 100
        lowest_temp_date = ""
        most_humidity = 0
        most_humid_day = ""
        prev_month = (str(self.__dated_weather_data[0]).split("-"))[1]
        for row in self.__dated_weather_data:
            date = row[0]
            max_temp = row[1]
            min_temp = row[2]
            humidity = row[3]
            d = date.split("-")
            curr_year = d[0]
            curr_month = d[1]
            if curr_year == _year and curr_month == _month:
                self.__specified_month_temp.append((d[2], max_temp, min_temp))
            max_temp_sum += max_temp
            min_temp_sum += min_temp
            humidity_sum += humidity
            days_in_month += 1
            if highest_temp < max_temp:
                highest_temp = max_temp
                highest_temp_date = d
            if lowest_temp > min_temp:
                lowest_temp = min_temp
                lowest_temp_date = d
            if most_humidity < humidity:
                most_humidity = humidity
                most_humid_day = d
            if days_in_month > 0 and prev_month != curr_month:
                prev_month = curr_month
                max_temp_avg = max_temp_sum / days_in_month
                min_temp_avg = min_temp_sum / days_in_month
                humidity_avg = humidity_sum / days_in_month
                days_in_month = 0
                max_temp_sum = 0
                min_temp_sum = 0
                humidity_sum = 0
                self.__monthly_avg_temp.append((d[0], d[1], round(max_temp_avg),
                                                round(min_temp_avg), round(humidity_avg)))
                highest_temp_tuple = (highest_temp_date[0],
                                      highest_temp_date[1],
                                      highest_temp_date[2], highest_temp)
                for year in self.__yearly_max_temp:
                    if year[0] == highest_temp_date[0] and \
                                    int(year[3]) < highest_temp:
                        self.__yearly_max_temp.remove(year)
                self.__yearly_max_temp.append(highest_temp_tuple)
                lowest_temp_tuple = (lowest_temp_date[0],
                                     lowest_temp_date[1],
                                     lowest_temp_date[2], lowest_temp)
                for year in self.__yearly_min_temp:
                    if year[0] == lowest_temp_date[0] and \
                                    int(year[3]) > lowest_temp:
                        self.__yearly_min_temp.remove(year)
                self.__yearly_min_temp.append(lowest_temp_tuple)
                most_humid_tuple = (most_humid_day[0],
                                    most_humid_day[1],
                                    most_humid_day[2], most_humidity)
                for year in self.__yearly_max_humidity:
                    if year[0] == most_humid_day[0] and \
                            int(year[3] < most_humidity):
                        self.__yearly_max_humidity.remove(year)
                self.__yearly_max_humidity.append(most_humid_tuple)
                highest_temp = 0
                highest_temp_date = ""
                lowest_temp = 100
                lowest_temp_date = ""
                most_humidity = 0
                most_humid_day = ""

        self.__yearly_max_temp.sort(key=lambda tup: tup[0])
        self.__yearly_min_temp.sort(key=lambda tup: tup[0])
        self.__yearly_max_humidity.sort(key=lambda tup: tup[0])

    def annual_report(self, year_str):
        for year in self.__yearly_max_temp:
            if year[0] == year_str:
                print("Highest:", year[3], "\bC on", calendar.month_name[int(year[1])], year[2])
                break
        for year in self.__yearly_min_temp:
            if year[0] == year_str:
                print("Lowest:", year[3], "\bC on", calendar.month_name[int(year[1])], year[2])
                break
        for year in self.__yearly_max_humidity:
            if year[0] == year_str:
                print("Humid:", year[3], "\b% on", calendar.month_name[int(year[1])], year[2])
                break

    def monthly_avg_report(self, y, m):
        for month in self.__monthly_avg_temp:
            if month[0] == y and month[1] == m:
                print("Highest Average:", month[2], "\bC")
                print("Lowest Average:", month[3], "\bC")
                print("Average Humidity:", month[4], "\b%")
                break

    def month_chart_dual(self):
        print(calendar.month_name[int(self.__month)], self.__year, end="")
        for day in self.__specified_month_temp:
            print("\033[1;31;47m")
            print(day[0], "+" * int(day[1]), day[1], "\bC", end="")
            print("\033[1;34;47m")
            print(day[0], "+" * int(day[2]), day[2], "\bC", end="")
        print("\n")

    def month_chart_bonus(self):
        print(calendar.month_name[int(self.__month)], self.__year)
        for day in self.__specified_month_temp:
            print("\033[1;30;47m", "{:2}".format(day[0]), end=" ")
            print("\033[1;34;47m", "+" * int(day[2]), sep="", end="")
            print("\033[1;31;47m", "+" * (int(day[1]) - int(day[2])), sep="", end="")
            print("\033[1;30;47m", day[2], "\bC -", day[1], "\bC")
        print("\n")


def main():
    args = len(sys.argv)
    if args == 4:
        option = str(sys.argv[1])
        term = str(sys.argv[2]).split("/")
        path = str(sys.argv[3])
        if option == "-c" or option == "-b":
            weather = Weather(path, term[0], term[1])
        else:
            weather = Weather(path)
        if option == "-e":
            weather.annual_report(term[0])
        elif option == "-a":
            weather.monthly_avg_report(term[0], term[1])
        elif option == "-c":
            weather.month_chart_dual()
        elif option == "-b":
            weather.month_chart_bonus()

if __name__ == '__main__':
    main()
