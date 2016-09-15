import os
import csv
import calendar
import argparse


def skip_last_line(it):
    prev = next(it)
    for item in it:
        yield prev
        prev = item


class Weather:
    dated_weather_data = []
    # date, maxTemp, minTemp, maxHumid
    month = ""
    year = ""
    specified_month_temp = []
    # day, maxT, minT
    monthly_avg_temp = []
    # year, month, avg_maxT, avg_minT, avg_maxH
    yearly_max_temp = []
    # year, month, day, maxTemp
    yearly_min_temp = []
    # year, month, day, minTemp
    yearly_max_humidity = []
    # year, month, day, maxHumidity

    def __init__(self):
        self.year = ""
        self.month = ""

    def read_data(self, path_to_dir):
        for root, dirs, files in os.walk(path_to_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path) as file:
                    next(file)
                    csv_file = csv.DictReader(file)
                    for line in skip_last_line(csv_file):
                        if not line["Min TemperatureC"] or \
                                        not line["Max TemperatureC"] or \
                                        not line["Max Humidity"]:
                            # Do not read this particular day if its -
                            # - missing values of Min or Max temp or humidity
                            continue
                        self.dated_weather_data.append((str(line.get("PKT") or
                                                            line.get("PKST")),
                                                        int(line.get("Max TemperatureC")),
                                                        int(line.get("Min TemperatureC")),
                                                        int(line.get("Max Humidity"))))

    def process_data(self, _year="", _month=""):
        self.month = _month
        self.year = _year
        days_in_month = max_temp_sum = min_temp_sum = humidity_sum = 0
        highest_temp = most_humidity = 0
        lowest_temp = 100
        highest_temp_date = lowest_temp_date = most_humid_day = ""
        prev_month = (str(self.dated_weather_data[0]).split("-"))[1]
        for row in self.dated_weather_data:
            date = row[0]
            max_temp = row[1]
            min_temp = row[2]
            humidity = row[3]
            d = date.split("-")
            curr_year = d[0]
            curr_month = d[1]
            if curr_year == _year and curr_month == _month:
                self.specified_month_temp.append((d[2], max_temp, min_temp))
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
                self.monthly_avg_temp.append((d[0], d[1], round(max_temp_sum / days_in_month),
                                              round(min_temp_sum / days_in_month),
                                              round(humidity_sum / days_in_month)))
                days_in_month = max_temp_sum = min_temp_sum = humidity_sum = 0
                Weather.append_yearly_data(self, "max", highest_temp_date, highest_temp)
                Weather.append_yearly_data(self, "min", lowest_temp_date, lowest_temp)
                Weather.append_yearly_data(self, "humid", most_humid_day, most_humidity)
                highest_temp = most_humidity = 0
                lowest_temp = 100
                highest_temp_date = lowest_temp_date = most_humid_day = ""
        Weather.sort_data(self)

    def append_yearly_data(self, option_str, date_str, value):
        temp_tuple = (date_str[0], date_str[1], date_str[2], value)
        if option_str == "max":
            for year in self.yearly_max_temp:
                if year[0] == date_str[0] and int(year[3]) < value:
                    self.yearly_max_temp.remove(year)
            self.yearly_max_temp.append(temp_tuple)
        elif option_str == "min":
            for year in self.yearly_min_temp:
                if year[0] == date_str[0] and int(year[3]) > value:
                    self.yearly_min_temp.remove(year)
            self.yearly_min_temp.append(temp_tuple)
        elif option_str == "humid":
            for year in self.yearly_max_humidity:
                if year[0] == date_str[0] and int(year[3]) < value:
                    self.yearly_max_humidity.remove(year)
            self.yearly_max_humidity.append(temp_tuple)

    def sort_data(self):
        self.yearly_max_temp.sort(key=lambda tup: tup[0])
        self.yearly_min_temp.sort(key=lambda tup: tup[0])
        self.yearly_max_humidity.sort(key=lambda tup: tup[0])

    def annual_report(self, year_str):
        for year in self.yearly_max_temp:
            if year[0] == year_str:
                print("Highest:", year[3], "\bC on", calendar.month_name[int(year[1])], year[2])
                break
        for year in self.yearly_min_temp:
            if year[0] == year_str:
                print("Lowest:", year[3], "\bC on", calendar.month_name[int(year[1])], year[2])
                break
        for year in self.yearly_max_humidity:
            if year[0] == year_str:
                print("Humid:", year[3], "\b% on", calendar.month_name[int(year[1])], year[2])
                break

    def monthly_avg_report(self, y, m):
        for month in self.monthly_avg_temp:
            if month[0] == y and month[1] == m:
                print("Highest Average:", month[2], "\bC")
                print("Lowest Average:", month[3], "\bC")
                print("Average Humidity:", month[4], "\b%")
                break

    def month_chart_dual(self):
        print(calendar.month_name[int(self.month)], self.year, end="")
        for day in self.specified_month_temp:
            print("\033[1;31;47m")
            print(day[0], "+" * int(day[1]), day[1], "\bC", end="")
            print("\033[1;34;47m")
            print(day[0], "+" * int(day[2]), day[2], "\bC", end="")
        print("\n")

    def month_chart_bonus(self):
        print(calendar.month_name[int(self.month)], self.year)
        for day in self.specified_month_temp:
            print("\033[1;30;47m", "{:2}".format(day[0]), end=" ")
            print("\033[1;34;47m", "+" * int(day[2]), sep="", end="")
            print("\033[1;31;47m", "+" * (int(day[1]) - int(day[2])), sep="", end="")
            print("\033[1;30;47m", day[2], "\bC -", day[1], "\bC")
        print("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", help="Annual Report of Extreme Weather", nargs=2)
    parser.add_argument("-a", help="Monthly average", nargs=2)
    parser.add_argument("-c", help="Monthly Bar Chart", nargs=2)
    parser.add_argument("-b", help="Bonus Chart", nargs=2)
    arg = parser.parse_args()
    weather = Weather()
    if arg.e:
        weather.read_data(arg.e[1])
        weather.process_data()
        weather.annual_report(arg.e[0])
    elif arg.a:
        weather.read_data(arg.a[1])
        weather.process_data()
        term = str(arg.a[0]).split("/")
        weather.monthly_avg_report(term[0], term[1])
    elif arg.c:
        term = str(arg.c[0]).split("/")
        weather.read_data(arg.c[1])
        weather.process_data(term[0], term[1])
        weather.month_chart_dual()
    elif arg.b:
        term = str(arg.b[0]).split("/")
        weather.read_data(arg.b[1])
        weather.process_data(term[0], term[1])
        weather.month_chart_bonus()

if __name__ == '__main__':
    main()
