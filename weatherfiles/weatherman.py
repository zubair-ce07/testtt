import csv
import fnmatch
import os
import calendar
import sys

try:
    mode = sys.argv[1]
    path = sys.argv[3]
    files = os.listdir(path)
    highest_temp = dict()
    min_temp = dict()
    max_humid = dict()
    print_mode = ""
    regex = ""
    blue = "\033[34m"
    red = "\033[31m"
    white = "\033[37m"

    if mode == "-e":
        print_mode = "temperature"
        file_year = sys.argv[2]
        regex = "*" + file_year + "*.txt"
    else:
        file_year = sys.argv[2].split("/")[0]
        file_month = sys.argv[2].split("/")[1]
        file_month = calendar.month_name[int(file_month)]
        regex = (
            "*"
            + file_year
            + "*"
            + file_month[0]
            + file_month[1]
            + file_month[2]
            + "*.txt"
        )
        if mode == "-a":
            print_mode = "temperature_average"

        elif mode == "-c":
            print_mode = "graph"

    def format_date(date_string):
        date_string = (
            calendar.month_name[int(date_string.split("-")[1])]
            + " "
            + date_string.split("-")[2]
        )
        return date_string

    def find_average(dictionary):
        length = len(dictionary.values())
        sum_of_values = 0
        for values in dictionary.values():
            sum_of_values = sum_of_values + values
        average_of_values = int(sum_of_values/length)
        return average_of_values


    for file in files:
        if fnmatch.fnmatch(file, regex):
            with open(path + "/" + file, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        first_key = list(row.keys())[0]
                        line_count += 1

                    if row["Max TemperatureC"] == "":
                        highest_temp[row[first_key]] = 0
                    else:
                        highest_temp[row[first_key]] = int(
                            row["Max TemperatureC"]
                        )

                    if row["Min TemperatureC"] == "":
                        min_temp[row[first_key]] = 0
                    else:
                        min_temp[row[first_key]] = int(row["Min TemperatureC"])

                    if row["Max Humidity"] == "":
                        max_humid[row[first_key]] = 0
                    else:
                        max_humid[row[first_key]] = int(row["Max Humidity"])
                    line_count += 1

    max_temp_value = max(highest_temp, key=highest_temp.get)
    min_temp_value = min(min_temp, key=min_temp.get)
    max_humid_value = max(max_humid, key=max_humid.get)

    if print_mode == "temperature":
        print(
            "Highest: "
            + str(highest_temp[max_temp_value])
            + "C on "
            + format_date(max_temp_value)
        )
        print(
            "Lowest: "
            + str(min_temp[min_temp_value])
            + "C on "
            + format_date(min_temp_value)
        )
        print(
            "Humid: "
            + str(max_humid[max_humid_value])
            + "% on "
            + format_date(max_humid_value)
        )
        
    elif print_mode == "temperature_average":
        average_highest_temp = find_average(highest_temp)
        average_lowest_temp = find_average(min_temp)
        average_humidity = find_average(max_humid)
        print(
            "Highest Average: "
            + str(average_highest_temp)
            + "C"
        )
        print(
            "Lowest Average: "
            + str(average_lowest_temp)
            + "C"
        )
        print(
            "Average Humidity: "
            + str(average_humidity)
            + "%"
        )

    elif print_mode == "graph":
        for key in highest_temp:
            if key in min_temp:
                highest_temp[key] = (
                    str(min_temp[key]) + "/" + str(highest_temp[key])
                )
            else:
                pass

        for key, value in highest_temp.items():
            day = key.split("-")[2]
            min_display = str(value.split("/")[0])
            max_display = str(value.split("/")[1])
            min_temp_graph = ""
            max_temp_graph = ""
            for i in range(int(min_display)):
                min_temp_graph = min_temp_graph + "+"
            for i in range(int(max_display)):
                max_temp_graph = max_temp_graph + "+"

            if len(day) == 1:
                day = "0" + day
            if len(min_display) == 1:
                min_display = "0" + min_display
            elif min_display.find("-") == 0:
                min_display = min_display.replace("-", "")
                min_display = "-" + "0" + min_display
            else:
                pass

            if len(max_display) == 1:
                max_display = "0" + max_display

            if sys.argv[2].split("/")[1][0] == "0":
                print(
                    day + " " + red + max_temp_graph, white + max_display + "C"
                )
                print(
                    day + " " + blue + min_temp_graph,
                    white + min_display + "C",
                )
            else:
                print(
                    day + " " + blue + min_temp_graph + red + max_temp_graph,
                    white + min_display + "C" + "-" + max_display + "C",
                )
except (IndexError, ValueError):
    print("Please enter a valid command or a valid file year/month.")
