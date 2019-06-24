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
    def print_year_result(self, max_temp, max_temp_date, min_temp,
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

    def print_month_result(self, avg_max_temp, avg_min_temp,
                           avg_mean_humidity):
        avg_max_temp = round(avg_max_temp, 2)
        print(f"Highest Average: {avg_max_temp}C")
        avg_min_temp = round(avg_min_temp, 2)
        print(f"Lowest Average: {avg_min_temp}C")
        avg_mean_humidity = round(avg_mean_humidity, 2)
        print(f"Average Mean Humidity: {avg_mean_humidity}%")

    def plot_bar(self, limit, color):
        for i in range(limit):
            print("{}+".format(color), end="")

    def print_month_year(self, data, year_index, month_index):
        time = data[year_index][month_index][0].date
        time = str_to_date(time)
        month_name = time.strftime("%B")
        year = time.strftime("%Y")
        print(f"{month_name} {year}")

    def plot_month_barchart(self, data, year_index, month_index):
        self.print_month_year(data, year_index, month_index)
        for i in range(0, len(data[year_index][month_index])):
            if data[year_index][month_index][i].max_temp:
                if i + 1 < 10:
                    print(u"\u001b[35m0", end="")
                print(u"\u001b[35m{}".format(i + 1), end=" ")
                self.plot_bar(int(data[year_index][month_index][i].max_temp),
                              u"\u001b[31m")
                print(u"\u001b[35m {}C".format(data[year_index][month_index][i]
                      .max_temp))

            if data[year_index][month_index][i].min_temp:
                if i + 1 < 10:
                    print(u"\u001b[35m0", end="")
                print(u"\u001b[35m{}".format(i + 1), end=" ")
                self.plot_bar(int(data[year_index][month_index][i].min_temp),
                              u"\u001b[36m")
                print(u"\u001b[35m {}C".format(data[year_index][month_index][i]
                                               .min_temp))
            print()

    def plot_component_barchart(self, data, year_index, month_index):
        self.print_month_year(data, year_index, month_index)
        for i in range(0, len(data[year_index][month_index])):
            if data[year_index][month_index][i].min_temp:
                if i + 1 < 10:
                    print(u"\u001b[35m0", end="")
                print(u"\u001b[35m{}".format(i + 1), end="")
                self.plot_bar(int(data[year_index][month_index][i].min_temp),
                              u"\u001b[36m")
            if data[year_index][month_index][i].max_temp:
                self.plot_bar(int(data[year_index][month_index][i].max_temp),
                              u"\u001b[31m")
                print(u"\u001b[35m {}C".format(data[year_index][month_index][i]
                      .min_temp), end="-")
                print(u"\u001b[35m{}C".format(data[year_index][month_index][i]
                                              .max_temp))


class WeatherAnalysis:
    def find_year_index(self, data, year):
        year_found = False
        index = 0
        for index in range(0, len(data[index])):
            time = data[index][0][0].date
            time = str_to_date(time)
            split_year = time.strftime("%Y")
            if int(split_year) == int(year):
                year_found = True
                break
        if not year_found:
            print("Record of this year does not exist in system")
            return -1

        return index

    def find_month_index(self, data, year_index, month):
        month_found = False
        for month_index in range(0, len(data[year_index])):
            time = data[year_index][month_index][0].date
            time = str_to_date(time)
            split_month = time.strftime("%m")
            if int(split_month) == int(month):
                month_found = True
                break
        if not month_found:
            print("Record of this month does not exist in system")
            return - 1

        return month_index

    def find_year_max_temp(self, data, index):
        max_temp = data[index][0][0].max_temp
        max_temp_date = data[index][0][0].date
        for i in range(0, len(data[index])):
            for j in range(0, len(data[index][i])):
                if not data[index][i][j].max_temp:
                    continue
                if int(data[index][i][j].max_temp) > int(max_temp):
                    max_temp = data[index][i][j].max_temp
                    max_temp_date = data[index][i][j].date
        year_data = {"value": max_temp,
                     "date": max_temp_date}

        return year_data

    def find_year_min_temp(self, data, index):
        min_temp = data[index][0][0].min_temp
        min_temp_date = data[index][0][0].date
        for i in range(0, len(data[index])):
            for j in range(0, len(data[index][i])):
                if not data[index][i][j].min_temp:
                    continue
                if int(data[index][i][j].min_temp) < int(min_temp):
                    min_temp = data[index][i][j].min_temp
                    min_temp_date = data[index][i][j].date
        year_data = {"value": min_temp,
                     "date": min_temp_date}

        return year_data

    def find_year_max_humidity(self, data, index):
        max_humidity = data[index][0][0].max_humidity
        max_humidity_date = data[index][0][0].date
        for i in range(0, len(data[index])):
            for j in range(0, len(data[index][i])):
                if not data[index][i][j].max_humidity:
                    continue
                if int(data[index][i][j].max_humidity) > int(max_humidity):
                    max_humidity = data[index][i][j].max_humidity
                    max_humidity_date = data[index][i][j].date
        year_data = {"value": max_humidity,
                     "date": max_humidity_date}

        return year_data

    def find_month_avg_max_temp(self, data, year_index, month_index):
        avg_max_temp = 0
        for i in range(0, len(data[year_index][month_index])):
            if not data[year_index][month_index][i].max_temp:
                    continue
            avg_max_temp += int(data[year_index][month_index][i].max_temp)
        avg_max_temp = avg_max_temp / len(data[year_index][month_index])

        return avg_max_temp

    def find_month_avg_min_temp(self, data, year_index, month_index):
        avg_min_temp = 0
        for i in range(0, len(data[year_index][month_index])):
            if not data[year_index][month_index][i].min_temp:
                    continue
            avg_min_temp += int(data[year_index][month_index][i].min_temp)
        avg_min_temp = avg_min_temp / len(data[year_index][month_index])

        return avg_min_temp

    def find_month_avg_mean_humidity(self, data, year_index, month_index):
        avg_mean_humidity = 0
        for i in range(0, len(data[year_index][month_index])):
            if not data[year_index][month_index][i].mean_humidity:
                    continue
            avg_mean_humidity += int(data[year_index][month_index][i]
                                     .mean_humidity)
        avg_mean_humidity /= len(data[year_index][month_index])

        return avg_mean_humidity


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


def read_tuple_data(row):
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


def parse_file():
    path = 'weatherfiles/weatherfiles'
    file_list = read_file_names(path)
    year_data = []
    month_data = []
    current_year = "2004"
    for files in file_list:
        day_data = []
        year_index = files.index("20")
        file_year = files[year_index: year_index+4]
        if(current_year != file_year):
            year_data.append(month_data)
            current_year = file_year
            month_data = []
        with open(files, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row_data = read_tuple_data(row)
                day_data.append(row_data)
        month_data.append(day_data)

    year_data.append(month_data)
    return year_data


def get_year_reading(data, year):
    year_analysis = WeatherAnalysis()
    index = year_analysis.find_year_index(data, year)
    if(index == -1):
        return
    max_temp_data = year_analysis.find_year_max_temp(data, index)
    min_temp_data = year_analysis.find_year_min_temp(data, index)
    max_humidity_data = year_analysis.find_year_max_humidity(data, index)
    year_data = {"max temp": max_temp_data,
                 "min temp": min_temp_data,
                 "max humidity": max_humidity_data}

    return year_data


def get_month_reading(data, month):
    month_analysis = WeatherAnalysis()
    year, month = month.split("/")
    year_index = month_analysis.find_year_index(data, year)
    if(year_index == -1):
        return
    month_index = month_analysis.find_month_index(data, year_index, month)
    if(month_index == -1):
        return

    avg_max_temp = month_analysis.find_month_avg_max_temp(
                                  data, year_index, month_index)
    avg_min_temp = month_analysis.find_month_avg_min_temp(
                                  data, year_index, month_index)
    avg_mean_hum = month_analysis.find_month_avg_mean_humidity(
                                  data, year_index, month_index)
    month_data = {"avg max temp": avg_max_temp,
                  "avg min temp": avg_min_temp,
                  "avg mean humidity": avg_mean_hum}

    return month_data


def get_month_graph(data, month):
    month_analysis = WeatherAnalysis()
    year, month = month.split("/")
    year_index = month_analysis.find_year_index(data, year)
    if(year_index == -1):
        return
    month_index = month_analysis.find_month_index(data, year_index, month)
    if(month_index == -1):
        return
    chart_data = {"year index": year_index,
                  "month index": month_index}

    return chart_data
