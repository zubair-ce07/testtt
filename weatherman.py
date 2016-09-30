import sys

import os

# class to save record of whole year in object oriented way


class TemperatureReport:
    date = ""
    maxTemperature = 0
    minTemperature = 0
    humidity = 0

    def __init__(self, date, max_temp, min_temp, humid):
        self.date = date
        self.maxTemperature = max_temp
        self.minTemperature = min_temp
        self.humidity = humid
# class temperature report ends here


class WeatherMan:
    def __init__(self):
        return

    @staticmethod
    def yearly_report(temp_file_list):
        temp_record = []
        day_of_highest = ""
        month_of_highest = ""
        high_temp = 0
        for temperature_file in temp_file_list:
            if os.path.isfile(filePathArg + "/" + temperature_file):
                f = open(filePathArg + "/" + temperature_file, 'r')
                f.readline()  # skipping 1st line containing empty space
                f.readline()  # skipping header line
                for line in f:
                    if line.startswith("<!"):  # skip last line
                        f.readline()
                    else:
                        line_element = line.split(',')  # split on ,
                        if line_element[1] == '':  # in case reading not taken
                            line_element[1] = 0
                        if line_element[7] == '':  # in case reading not taken
                            line_element[7] = 0
                        # save 365 records in list
                        temp_record.append(
                            TemperatureReport(line_element[0],
                                              int(line_element[1]),
                                              line_element[3],
                                              int(line_element[7]))
                        )

                high_temp_date = ""
                for temp in temp_record:  # iterating through each object
                    if temp.maxTemperature >= high_temp:
                        high_temp = temp.maxTemperature
                        high_temp_date = temp.date
                date_to_month = high_temp_date.split('-')
                month_of_highest = int(date_to_month[1])
                day_of_highest = date_to_month[2]
        print("Highest: "+str(high_temp) +
              "C on " + year_month[month_of_highest-1] +
              " "+str(day_of_highest))

        low_temp = 40            # random value just to compare mintemp
        low_temp_date = ""
        for temp in temp_record:
                if temp.minTemperature != '':
                    if int(temp.minTemperature) <= int(low_temp):
                        low_temp = temp.minTemperature
                        low_temp_date = temp.date
        date_to_month = low_temp_date.split('-')
        month_of_lowest = int(date_to_month[1])
        day_of_lowest = date_to_month[2]
        print("Lowest: " + str(low_temp) + "C on " +
              year_month[month_of_lowest - 1] + " " +
              str(day_of_lowest))

        most_humidity = 0
        most_humid_day = ""
        for temp in temp_record:
                    if int(temp.humidity) >= int(most_humidity):
                        most_humidity = temp.humidity
                        most_humid_day = temp.date
        date_to_month = most_humid_day.split('-')
        month_of_humidity = int(date_to_month[1])
        day_of_humidity = date_to_month[2]
        print("Humidity: " + str(most_humidity) +
              "% on " + year_month[month_of_humidity - 1] +
              " " + str(day_of_humidity))

    @staticmethod
    def monthly_report(temp_filename):
        if os.path.isfile(filePathArg + "/" + temp_filename):
            f = open(filePathArg + "/" + temp_filename, 'r')
            highest_average_array = []
            lowest_average_array = []
            average_mean_humidity = []
            f.readline()
            f.readline()

            for line in f:
                if line.startswith("<!"):
                    f.readline()
                else:
                    line_element = line.split(',')
                    if line_element[1] != '':
                        highest_average_array.append(int(line_element[1]))
                    if line_element[3] != '':
                        lowest_average_array.append(int(line_element[3]))
                    if line_element[8] != '':
                        average_mean_humidity.append(int(line_element[8]))
            # calculating average
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
            f.readline()
            f.readline()
            day_counter = 1
            for line in f:
                red_text = ""
                blue_text = ""
                if line.startswith("<!"):
                    f.readline()
                else:
                    line_element = line.split(',')  # reading not taken
                    if line_element[1] != '':
                        highest_temp = line_element[1]
                        for i in range(0, int(highest_temp)):
                            red_text += "+"
                        red_color_bar = "\033[1;31m" + red_text + "\033[1;m"
                        print(str(day_counter) + red_color_bar + highest_temp)

                    if line_element[3] != '':
                        lowest_temp = line_element[3]
                        for i in range(0, int(lowest_temp)):
                            blue_text += "+"
                        blue_color_bar = "\033[1;34m" + blue_text + "\033[1;m"
                        print(str(day_counter) + blue_color_bar + lowest_temp)
                    day_counter += 1
            return

    @staticmethod
    def one_line_chart_report(temp_filename):
        if os.path.isfile(filePathArg + "/" + temp_filename):
            f = open(filePathArg + "/" + temp_filename, 'r')
            highest_temp = ""
            f.readline()
            f.readline()
            red_color_bar = ""
            day_counter = 1
            for line in f:
                red_text = ""
                blue_text = ""
                if line.startswith("<!"):
                    f.readline()
                else:
                    line_element = line.split(',')  # reading not taken
                    if line_element[1] != '':
                        highest_temp = line_element[1]

                        for i in range(0, int(highest_temp)):
                            red_text += "+"
                        red_color_bar = "\033[1;31m" + red_text + "\033[1;m"
                    if line_element[3] != '':
                        lowest_temp = line_element[3]
                        for i in range(0, int(lowest_temp)):
                            blue_text += "+"
                        blue_color_bar = "\033[1;34m" + blue_text + "\033[1;m"
                        print(str(day_counter) +
                              blue_color_bar +
                              red_color_bar +
                              lowest_temp + "-" +
                              highest_temp)
                    day_counter += 1

            return

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
if len(sys.argv) == 1:  # in case user run program from ide
    report_type = raw_input("Please enter flag value: ")  # manual input
else:
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
