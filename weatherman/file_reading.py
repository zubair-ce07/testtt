import glob
import calendar
import csv


def file_reading(dir, month, year):
    FILE_NAME = glob.glob(dir + "/*_weather_" +
                          str(year) + "_" + str(month) + "*")
    if FILE_NAME:
        FILE_READER = open(FILE_NAME[0])
        return csv.DictReader(FILE_READER)


def data_reading(dir, month, year):
    MONTHS = []
    if month:
        MONTHS = [calendar.month_abbr[int(month)]]
    else:
        MONTHS = [calendar.month_abbr[i] for i in range(1, 13)]
    oerder_dict = []
    complete_data = []
    for month in MONTHS:
        FILE_READER = file_reading(dir, month, year)
        if FILE_READER:
            for line in FILE_READER:
                oerder_dict.append(line)
            complete_data.append(oerder_dict)
    return complete_data
