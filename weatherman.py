import sys

import os

import csv

# class to save record of whole year in object oriented way


class TemperatureReport:
    date = ""
    max_temperature = 0
    min_temperature = 0
    humidity = 0

    def __init__(self, date, max_temp, min_temp, humid):
        self.date = date
        self.max_temperature = max_temp
        self.min_temperature = min_temp
        self.humidity = humid
# class temperature report ends here


class WeatherMan:
    def __init__(self):
        return

    @staticmethod
    def yearly_report(temp_file_list):
        temp_records = []
        day_of_highest = ""
        month_of_highest = ""
        high_temp = 0
        for temperature_file in temp_file_list:
            if os.path.isfile(filePathArg + "/" + temperature_file):
                f = open(filePathArg + "/" + temperature_file, 'r')
                try:
                    with f as csvfile:
                        next(csvfile)  # skip first empty line
                        reader = csv.DictReader(
                            filter(lambda row: row[0] != '<', csvfile)
                                                )
                        header = reader.fieldnames
                        for row in reader:
                            # reading not taken
                            if row['Max TemperatureC'] == '':
                                row['Max TemperatureC'] = 0
                            # reading not taken
                            if row['Max Humidity'] == '':
                                row['Max Humidity'] = 0
                            temp_records.append(
                                TemperatureReport(row[header[0]],
                                                  int(row['Max TemperatureC']),
                                                  row['Min TemperatureC'],
                                                  int(row["Max Humidity"]))
                            )
                finally:
                    f.close()
                high_temp_date = ""
                # iterating through each object
                for temp_record in temp_records:
                    if temp_record.max_temperature >= high_temp:
                        high_temp = temp_record.max_temperature
                        high_temp_date = temp_record.date
                date_to_month = high_temp_date.split('-')
                month_of_highest = int(date_to_month[1])
                day_of_highest = date_to_month[2]
        print("Highest: "+str(high_temp) +
              "C on " + year_month[month_of_highest-1] +
              " "+str(day_of_highest))

        low_temp = high_temp    # random value just to compare mintemp
        low_temp_date = ""
        for temp_record in temp_records:
                if temp_record.min_temperature != '':
                    if temp_record.min_temperature != '' and \
                       int(temp_record.min_temperature) <= int(low_temp):
                        low_temp = temp_record.min_temperature
                        low_temp_date = temp_record.date
        date_to_month = low_temp_date.split('-')
        month_of_lowest = int(date_to_month[1])
        day_of_lowest = date_to_month[2]
        print("Lowest: " + str(low_temp) + "C on " +
              year_month[month_of_lowest - 1] + " " +
              str(day_of_lowest))

        max_humidity = 0
        most_humid_day = ""
        for temp_record in temp_records:
                    if int(temp_record.humidity) >= int(max_humidity):
                        max_humidity = temp_record.humidity
                        most_humid_day = temp_record.date
        date_to_month = most_humid_day.split('-')
        month_of_humidity = int(date_to_month[1])
        day_of_humidity = date_to_month[2]
        print("Humidity: " + str(max_humidity) +
              "% on " + year_month[month_of_humidity - 1] +
              " " + str(day_of_humidity))

    @staticmethod
    def monthly_report(temp_filename):
        if os.path.isfile(filePathArg + "/" + temp_filename):
            f = open(filePathArg + "/" + temp_filename, 'r')
            highest_average_array = []
            lowest_average_array = []
            average_mean_humidity = []
            try:
                with f as csvfile:
                    next(csvfile)  # skip first empty line
                    reader = csv.DictReader(
                        filter(lambda row: row[0] != '<', csvfile)
                    )
                    header = reader.fieldnames
                    for row in reader:
                        if row['Max TemperatureC'] != '':
                            highest_average_array.append(int(row[header[1]]))
                        if row['Min TemperatureC'] != '':
                            lowest_average_array.append(int(row[header[3]]))
                        if row[' Mean Humidity'] != '':
                            average_mean_humidity.append(int(row[header[8]]))
            finally:
                f.close()

            highest_average = \
                int(sum(highest_average_array) / len(highest_average_array))
            lowest_average = \
                int(sum(lowest_average_array) / len(lowest_average_array))
            average_mean_humidity = \
                int(sum(average_mean_humidity) / len(average_mean_humidity))

            # printing
            print("Highest Average: " + str(highest_average) + "C")
            print("Lowest Average : " + str(lowest_average) + "C")
            print ("Average Mean Humidity: " +
                   str(average_mean_humidity) + "%")

    @staticmethod
    def chart_report(temp_filename):
        if os.path.isfile(filePathArg + "/" + temp_filename):
            f = open(filePathArg + "/" + temp_filename, 'r')
            day_counter = 1
            try:
                with f as csvfile:
                    next(csvfile)  # skip first empty line
                    reader = csv.DictReader(
                        filter(lambda row: row[0] != '<', csvfile)
                    )
                    header = reader.fieldnames
                    for row in reader:
                        red_text = ""
                        blue_text = ""
                        if row['Max TemperatureC'] != '':
                            highest_temp = int(row['Max TemperatureC'])
                            for i in range(0, int(highest_temp)):
                                red_text += "+"
                            red_color_bar = "\033[1;31m" + \
                                            red_text +\
                                            "\033[1;m"
                            print(str(day_counter) +
                                  red_color_bar +
                                  str(highest_temp))
                        if row['Min TemperatureC'] != '':
                            lowest_temp = int(row['Min TemperatureC'])
                            for i in range(0, int(lowest_temp)):
                                blue_text += "+"
                            blue_color_bar = "\033[1;34m" + \
                                             blue_text +\
                                             "\033[1;m"
                            print(str(day_counter) +
                                  blue_color_bar +
                                  str(lowest_temp))
                        day_counter += 1

            finally:
                f.close()

            return

    @staticmethod
    def one_line_chart_report(temp_filename):
        if os.path.isfile(filePathArg + "/" + temp_filename):
            f = open(filePathArg + "/" + temp_filename, 'r')
            highest_temp = ""
            red_color_bar = ""
            day_counter = 1
            try:
                with f as csvfile:
                    next(csvfile)  # skip first empty line
                    reader = csv.DictReader(
                        filter(lambda row: row[0] != '<', csvfile)
                    )
                    header = reader.fieldnames
                    for row in reader:
                        red_text = ""
                        blue_text = ""
                        if row['Max TemperatureC'] != '':
                            highest_temp = row['Max TemperatureC']

                            for i in range(0, int(highest_temp)):
                                red_text += "+"
                            red_color_bar = "\033[1;31m" + \
                                            red_text + "\033[1;m"
                        if row['Min TemperatureC'] != '':
                            lowest_temp = row['Min TemperatureC']
                            for i in range(0, int(lowest_temp)):
                                blue_text += "+"
                            blue_color_bar = "\033[1;34m" + \
                                             blue_text + "\033[1;m"
                            print(str(day_counter) + blue_color_bar +
                                  red_color_bar + lowest_temp + "-" +
                                  highest_temp)
                            day_counter += 1

            finally:
                    f.close()

                    return

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print ("Arguments are not valid")

        # more detail of error
        if len(sys.argv) == 3:
            print ("filename may be missing")
            sys.exit()
        else:
            if len(sys.argv) == 2:
                print ("date and filename missing")
                sys.exit()
            else:
                if len(sys.argv) == 1:
                    print ("report type,date and filename missing")
                    sys.exit()
    report_type = ""
    year = ""
    month = ""
    day = ""
    year_month = ["Jan", "Feb", "Mar", "Apr",
                  "May", "Jun", "Jul", "Aug",
                  "Sep", "Oct", "Nov", "Dec"
                  ]
    filePathArg = str(sys.argv[3])
    report_type = str(sys.argv[1])  # value coming from cmd

    if report_type == "-e":
        year = str(sys.argv[2])                          # calculating year
        if len(sys.argv[2].split('/')) > 1:
            print ("invalid arguments")
            sys.exit()
        if int(year) > 2011:
            print("record not found for this year")
            sys.exit()
        if int(year) < 1996:
            print("record not found for this year")
            sys.exit()
        file_list = []  # if year calculate from (12 files)list
        for month in year_month:
            file_prefix = "lahore_weather_" + year +\
                        "_"+month+".txt"  # creating temperature_file name
            file_list.append(file_prefix)
        WeatherMan().yearly_report(file_list)    # passing files to function

    else:
        if report_type == "-a":                      # monthly report
            yearPlusMonth = str(sys.argv[2]).split('/')
            if len(yearPlusMonth) < 2:
                print("invalid month")
                sys.exit()
            year = yearPlusMonth[0]
            month = int(yearPlusMonth[1])
            if month > 12:
                print("invalid month")
                sys.exit()
            if month < 1:
                print("invalid month")
                sys.exit()
            filename = "lahore_weather_" + year + "_" + \
                       str(year_month[(month-1)]) + ".txt"
            WeatherMan().monthly_report(filename)

        else:
            if report_type == "-c":
                yearPlusMonth = str(sys.argv[2]).split('/')
                if len(yearPlusMonth) < 2:
                    print("invalid month")
                    sys.exit()
                year = yearPlusMonth[0]
                month = int(yearPlusMonth[1])
                if month > 12:
                    print("invalid month")
                    sys.exit()
                if month < 1:
                    print("invalid month")
                    sys.exit()
                file_name = "lahore_weather_" +\
                            year + "_" + \
                            str(year_month[(month - 1)]) + \
                            ".txt"
                print(str(year_month[(month - 1)]) + " "+year)
                WeatherMan().chart_report(file_name)
            else:
                if report_type == "-c4":
                    yearPlusMonth = str(sys.argv[2]).split('/')
                    if len(yearPlusMonth) < 2:
                        print("invalid month")
                        sys.exit()
                    year = yearPlusMonth[0]
                    month = int(yearPlusMonth[1])
                    if month > 12:
                        print("invalid month")
                        sys.exit()
                    if month < 1:
                        print("invalid month")
                        sys.exit()
                    filename = "lahore_weather_" + \
                               year + "_" + \
                               str(year_month[(month - 1)]) + \
                               ".txt"
                    print(str(year_month[(month - 1)]) + " " + year)
                    WeatherMan().one_line_chart_report(filename)
                else:
                    print ("invalid arguments")
                    sys.exit()
