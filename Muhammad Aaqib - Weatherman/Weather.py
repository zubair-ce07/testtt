import os
import csv
import datetime


class WeatherReading:
    def __init__(self, date, max_temp, min_temp, max_humidity, mean_humidity):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity


class ResultPrinter:
    def print_annual_stats(self, max_temp, max_temp_date, min_temp,
                           min_temp_date, max_humidity, max_humidity_date):
        max_temp_date = str_to_date(max_temp_date)
        max_temp_day = max_temp_date.strftime("%B")
        split_date = max_temp_date.strftime("%d")
        print(f"Highest: {max_temp}C on {max_temp_day} {split_date}")
        min_temp_date = str_to_date(min_temp_date)
        min_temp_day = min_temp_date.strftime("%B")
        split_date = min_temp_date.strftime("%d")
        print(f"Lowest: {min_temp}C on {min_temp_day} {split_date}")
        max_humidity_date = str_to_date(max_humidity_date)
        max_humidity_day = max_humidity_date.strftime("%B")
        split_date = max_humidity_date.strftime("%d")
        print(f"Humidity: {max_humidity}% on {max_humidity_day} {split_date}")

    def print_annual_report(self, annual_stats):
        max_temp_obj = annual_stats.get("max temp")
        min_temp_obj = annual_stats.get("min temp")
        max_humidity_obj = annual_stats.get("max humidity")
        max_temp = max_temp_obj.max_temp
        max_temp_date = max_temp_obj.date
        min_temp = min_temp_obj.min_temp
        min_temp_date = min_temp_obj.date
        max_humidity = max_humidity_obj.max_humidity
        max_humidity_date = max_humidity_obj.date
        self.print_annual_stats(max_temp, max_temp_date, min_temp,
                                min_temp_date, max_humidity, max_humidity_date)

    def print_monthly_stats(self, avg_max_temp, avg_min_temp,
                            avg_mean_humidity):
        avg_max_temp = round(avg_max_temp, 2)
        print(f"Highest Average: {avg_max_temp}C")
        avg_min_temp = round(avg_min_temp, 2)
        print(f"Lowest Average: {avg_min_temp}C")
        avg_mean_humidity = round(avg_mean_humidity, 2)
        print(f"Average Mean Humidity: {avg_mean_humidity}%")

    def print_monthly_report(self, monthly_stats):
        avg_max_temp = monthly_stats.get("avg max temp")
        avg_min_temp = monthly_stats.get("avg min temp")
        avg_mean_humidity = monthly_stats.get("avg mean humidity")
        self.print_monthly_stats(avg_max_temp, avg_min_temp, avg_mean_humidity)

    def plot_bar(self, limit, color):
        for i in range(limit):
            print("{}+".format(color), end="")

    def print_month_and_year(self, month_data):
        time = month_data[0].date
        time = str_to_date(time)
        month_name = time.strftime("%B")
        year = time.strftime("%Y")
        print(f"{month_name} {year}")

    def print_day(self, day_record):
        day = day_record.date
        day = str_to_date(day)
        day = day.strftime("%d")
        print(u"\u001b[35m{}".format(day), end=" ")

    def print_temp(self, temp, end_with):
        print(u"\u001b[35m {}C".format(temp), end=end_with)

    def plot_month_barchart(self, chart_data):
        self.print_month_and_year(chart_data)
        for day_record in chart_data:
            if not day_record.max_temp:
                continue
            self.print_day(day_record)
            self.plot_bar(int(day_record.max_temp), u"\u001b[31m")
            self.print_temp(day_record.max_temp, "\n")
            self.print_day(day_record)
            self.plot_bar(int(day_record.min_temp), u"\u001b[36m")
            self.print_temp(day_record.min_temp, "\n\n")

    def plot_component_barchart(self, chart_data):
        self.print_month_and_year(chart_data)
        for day_record in chart_data:
            if not day_record.min_temp:
                continue
            self.print_day(day_record)
            self.plot_bar(int(day_record.min_temp), u"\u001b[36m")
            if not day_record.max_temp:
                continue
            self.plot_bar(int(day_record.max_temp), u"\u001b[31m")
            self.print_temp(day_record.min_temp, "-")
            self.print_temp(day_record.max_temp, "\n")


class WeatherAnalysis:
    def find_year(self, year_data, year):
        for month_data in year_data:
            for day_record in month_data:
                split_year = date_to_year(day_record.date)
                if split_year == year:
                    return True
                else:
                    return False

    def find_annual_stats(self, weather_record, year):
        year_found = False
        year_record = []
        for year_data in weather_record:
            year_found = self.find_year(year_data, year)
            if year_found:
                year_record = year_data
                break
        if not year_record:
            print("Record of this year does not exist in system")

        return year_record

    def find_month(self, month_data, month):
        for day_record in month_data:
            split_month = date_to_month(day_record.date)
            if int(split_month) == int(month):
                return True
            else:
                return False

    def find_monthly_stats(self, year_record, month):
        month_found = False
        month_record = []
        for month_data in year_record:
            month_found = self.find_month(month_data, month)
            if month_found:
                month_record = month_data
                break
        if not month_record:
            print("Record of this month does not exist in system")

        return month_record

    def find_year_max_temp(self, year_record):
        max_temp_obj = year_record[0][0]
        for month_record in year_record:
            for day_record in month_record:
                if not day_record.max_temp:
                    continue
                if int(day_record.max_temp) > int(max_temp_obj.max_temp):
                    max_temp_obj = day_record

        return max_temp_obj

    def find_year_min_temp(self, year_record):
        min_temp_obj = year_record[0][0]
        for month_record in year_record:
            for day_record in month_record:
                if not day_record.min_temp:
                    continue
                if int(day_record.min_temp) < int(min_temp_obj.min_temp):
                    min_temp_obj = day_record

        return min_temp_obj

    def find_year_max_humidity(self, year_record):
        max_humidity_obj = year_record[0][0]
        for month_record in year_record:
            for day_record in month_record:
                if not day_record.max_humidity:
                    continue
                if int(day_record.max_humidity) > int(max_humidity_obj.
                                                      max_humidity):
                    max_humidity_obj = day_record

        return max_humidity_obj

    def find_month_avg_max_temp(self, month_record):
        avg_max_temp = 0
        for day_record in month_record:
            if not day_record.max_temp:
                    continue
            avg_max_temp += int(day_record.max_temp)
        avg_max_temp /= len(month_record)

        return avg_max_temp

    def find_month_avg_min_temp(self, month_record):
        avg_min_temp = 0
        for day_record in month_record:
            if not day_record.min_temp:
                    continue
            avg_min_temp += int(day_record.min_temp)
        avg_min_temp /= len(month_record)

        return avg_min_temp

    def find_month_avg_mean_humidity(self, month_record):
        avg_mean_humidity = 0
        for day_record in month_record:
            if not day_record.mean_humidity:
                    continue
            avg_mean_humidity += int(day_record.mean_humidity)
        avg_mean_humidity /= len(month_record)

        return avg_mean_humidity


def date_to_year(date):
    date = str_to_date(date)
    split_year = date.strftime("%Y")
    return split_year


def date_to_month(date):
    date = str_to_date(date)
    split_month = date.strftime("%m")
    return split_month


def str_to_date(date):
    year, month, day = date.split("-")
    date = datetime.date(int(year), int(month), int(day))
    return date


def to_month_name(date):
    month_no = int(date.split("-")[1])
    month_name = ["January", "February", "March", "April", "May",
                  "June", "July", "August", "September", "October",
                  "November", "December"]
    return month_name[month_no - 1]


def read_file_names(path):
    file_list = []
    for root, directories, files in os.walk(path):
        for file in sorted(files):
            if '.txt' in file:
                file_list.append(os.path.join(root, file))

    return file_list


def read_tuple(row):
    max_temp = row['Max TemperatureC']
    min_temp = row['Min TemperatureC']
    max_humidity = row['Max Humidity']
    mean_humidity = row[' Mean Humidity']
    if "PKT" in row:
        date = (row["PKT"])
    else:
        date = (row["PKST"])
    row_data = WeatherReading(date, max_temp, min_temp,
                              max_humidity, mean_humidity)

    return row_data


def read_month_data(files):
    day_record = []
    with open(files, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row_data = read_tuple(row)
                day_record.append(row_data)
    return day_record


def parse_file():
    path = 'weatherfiles/weatherfiles'
    file_list = read_file_names(path)
    year_data = []
    month_data = []
    current_year = "2004"
    for files in file_list:
        year_index = files.index("20")
        file_year = files[year_index: year_index+4]
        if(current_year != file_year):
            year_data.append(month_data)
            current_year = file_year
            month_data = []
        day_record = read_month_data(files)
        month_data.append(day_record)

    year_data.append(month_data)
    return year_data


def get_annual_stats(weather_record, year):
    year_analysis = WeatherAnalysis()
    year_record = year_analysis.find_annual_stats(weather_record, year)
    if(not year_record):
        return
    max_temp_data = year_analysis.find_year_max_temp(year_record)
    min_temp_data = year_analysis.find_year_min_temp(year_record)
    max_humidity_data = year_analysis.find_year_max_humidity(year_record)
    annual_stats = {"max temp": max_temp_data,
                    "min temp": min_temp_data,
                    "max humidity": max_humidity_data}

    return annual_stats


def get_monthly_stats(weather_record, month):
    month_analysis = WeatherAnalysis()
    year, month = month.split("/")
    year_record = month_analysis.find_annual_stats(weather_record, year)
    if(not year_record):
        return
    month_record = month_analysis.find_monthly_stats(year_record, month)
    if(not month_record):
        return

    avg_max_temp = month_analysis.find_month_avg_max_temp(month_record)
    avg_min_temp = month_analysis.find_month_avg_min_temp(month_record)
    avg_mean_hum = month_analysis.find_month_avg_mean_humidity(month_record)
    monthly_stats = {"avg max temp": avg_max_temp,
                     "avg min temp": avg_min_temp,
                     "avg mean humidity": avg_mean_hum}

    return monthly_stats


def get_chart_data(weather_record, month):
    month_analysis = WeatherAnalysis()
    year, month = month.split("/")
    year_record = month_analysis.find_annual_stats(weather_record, year)
    if(not year_record):
        return
    month_record = month_analysis.find_monthly_stats(year_record, month)
    if(not month_record):
        return

    return month_record
