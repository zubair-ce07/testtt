"""This module give weather details
"""
import sys
from datetime import datetime, timedelta

COLOR_BLUE = '\033[94m'
COLOR_RED = '\033[91m'
COLOR_ENDC = '\033[0m'

CITY = "lahore"


def read_file_line(file_pointer, path, date):
    """The following function open the file if not opened.
    First two lines are not used so they are skipped.
    Return the file line and the file pointer
    """
    if file_pointer is None:
        filepath = "%s/%s_weather_%s_%s.txt" % (path,
                                                CITY,
                                                date.strftime("%Y"),
                                                date.strftime("%b"))
        file_pointer = open(filepath)
        file_pointer.readline()
        file_pointer.readline()
    return [file_pointer.readline(), file_pointer]


def get_month_day(date):
    """Split the date string by "-" and use it to make an instance of date.
    return date of format Month day i.e Jun 12
    """
    year, month, day = date.split("-")
    date = datetime(int(year), int(month), int(day))
    return "%s %s" % (date.strftime("%B"), date.strftime("%d"))


def year_details(year, path):
    """For a given year display the highest temperature and day,
    lowest temperature and day, most humid day and humidity
    """
    start_year = datetime(int(year), 1, 1)
    end_year = datetime(int(year)+1, 1, 1)
    delta = timedelta(days=31)
    max_temperature_record = []
    lowest_temperature_record = []
    max_humidity_record = []

    file_pointer = None
    while start_year < end_year:
        try:
            line, file_pointer = read_file_line(file_pointer, path, start_year)
            while line:
                data = line.split(",")
                if len(data) == 23:
                    if (not max_temperature_record or
                            int(data[1]) > int(max_temperature_record[1])):
                        max_temperature_record = data

                    if (not lowest_temperature_record or
                            int(data[3]) < int(lowest_temperature_record[3])):
                        lowest_temperature_record = data

                    if (not max_humidity_record or
                            int(data[7]) > int(max_humidity_record[7])):
                        max_humidity_record = data
                line, file_pointer = read_file_line(
                    file_pointer, path, start_year)

        except IOError:
            pass

        start_year += delta
        file_pointer = None
    print ("Highest: %sC on %s" % (max_temperature_record[1],
                                   get_month_day(max_temperature_record[0])))
    print ("Lowest: %sC on %s" % (lowest_temperature_record[3],
                                  get_month_day(lowest_temperature_record[0])))
    print ("Humid: %s%% on %s" % (max_humidity_record[7],
                                  get_month_day(max_humidity_record[0])))


def month_average_detail(date, path):
    """For a given month display the average highest temperature,
    average lowest temperature, average humidity.
    """
    year, month = date.split("/")
    date = datetime(int(year), int(month), 1)
    average_max_temperature_record = []
    average_lowest_temperature_record = []
    average_max_humidity_record = []
    file_pointer = None
    try:
        line, file_pointer = read_file_line(file_pointer, path, date)
        while line:
            data = line.split(",")
            if len(data) == 23:
                if (not average_max_temperature_record or
                        int(data[2]) > int(average_max_temperature_record[2])):
                    average_max_temperature_record = data

                if (not average_lowest_temperature_record or
                        int(data[2]) < int(average_lowest_temperature_record[3])):
                    average_lowest_temperature_record = data

                if (not average_max_humidity_record or
                        int(data[8]) > int(average_max_humidity_record[8])):
                    average_max_humidity_record = data
            line, file_pointer = read_file_line(file_pointer, path, date)

        print "%s %s" % (date.strftime("%B"), date.strftime("%Y"))

        print "Highest Average: %sC" % (average_max_temperature_record[2])
        print "Lowest Average: %sC" % (average_lowest_temperature_record[2])
        print "Average Humid: %s%%" % (average_max_humidity_record[8])

    except IOError:
        pass


def month_horizontal_chart(date, path):
    """For a given month draw two horizontal bar charts on the console
    for the highest and lowest temperature on each day.
    Highest in red and lowest in blue.
    """
    year, month = date.split("/")
    date = datetime(int(year), int(month), 1)
    delta = timedelta(days=1)
    mode_temp = sys.argv[1]
    file_pointer = None
    print "%s %s" % (date.strftime("%B"), date.strftime("%Y"))

    try:
        line, file_pointer = read_file_line(file_pointer, path, date)
        while line:
            data = line.split(",")
            if len(data) == 23:
                print "%s " % (date.strftime("%d")),
                for _ in range(int(data[3])):
                    print "%s+%s" % (COLOR_BLUE, COLOR_ENDC),

                if mode_temp == '-d':
                    print " %s\n%s " % (data[3], date.strftime("%d")),

                for _ in range(int(data[1])):
                    print "%s+%s" % (COLOR_RED, COLOR_ENDC),

                if mode_temp == '-d':
                    print " %s" % (data[1])
                else:
                    print "%sC - %sC " % (data[3], data[1])
            date += delta
            line = file_pointer.readline()

    except IOError:
        pass


if __name__ == "__main__":

    TASKS = {
        "-e": year_details,
        "-a": month_average_detail,
        "-c": month_horizontal_chart,
        "-d": month_horizontal_chart,
    }
    MODE, DATE, PATH = [sys.argv[1], sys.argv[2], sys.argv[3]]
    TASKS[MODE](DATE, PATH)
