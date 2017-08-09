import os
import csv
import operator
import datetime
import argparse
from termcolor import colored, cprint
from calendar import month_abbr


def renaming_and_conversion(year_month, first_argument, path):

    f_names = []

    for wt in os.listdir(path):

        w_cym, w_ext = os.path.splitext(wt)
        w_city, w_wthr, w_year, w_month = w_cym.split('_')

        if first_argument == '-e':

            if w_year == year_month:
                f_names.append(wt)
                return f_names

        elif first_argument == '-a' or first_argument == '-c':
            y = str(year_month)
            year, month = y.split("/")

            if w_year == year and w_month == month_abbr[int(month)]:
                f_names.append(wt)
                fnames = str(f_names[0])
                return fnames


def readf_content(path, fnames):
    with open(path + "/" + fnames) as f_content:
        filenum = csv.DictReader(f_content)
        answer = {}
        for row in filenum:
            for column, value in row.items():
                answer.setdefault(column, []).append(value)
    return answer


def get_weather_by_year(fnames):

    max_temp_month = []
    min_temp_month = []
    hu_mid_month = []
    date = []

    for f_content in fnames:
        answer = readf_content(arg, f_content)

        date_max = filter(None, answer.get("PKT"))
        for a in date_max:
            w_year, w_month, w_date = a.split('-')
            monthinteger = int(w_month)
            month = datetime.date(1900, monthinteger, 1).strftime('%B')
            final_date = month + " " + w_date + "  "
            date += {final_date}

        max_l = filter(None, answer.get("Max TemperatureC"))
        max_l = [int(i) for i in max_l]
        max_temp_month.append(max_l)

        min_l = filter(None, answer.get("Min TemperatureC"))
        min_l = [int(i) for i in min_l]
        min_temp_month.append(min_l)

        hu_mid_l = filter(None, answer.get("Max Humidity"))
        hu_mid_l = [int(i) for i in hu_mid_l]
        hu_mid_month.append(hu_mid_l)

    index, value = max(enumerate(max_temp_month), key=operator.itemgetter(1))
    print("Highest: ", value, "C on ", date[index])
    index, value = min(enumerate(min_temp_month), key=operator.itemgetter(1))
    print("Lowest: ", value, "C on ", date[index])
    index, value = max(enumerate(hu_mid_month), key=operator.itemgetter(1))
    print("Humid: ", value, "% on ", date[index])


def get_weather_by_month(answer):

    max_l = filter(None, answer.get("Max TemperatureC"))
    max_l = [int(i) for i in max_l]
    min_l = filter(None, answer.get("Min TemperatureC"))
    min_l = [int(i) for i in min_l]
    avg_humidity = filter(None, answer.get("Mean Humidity"))
    avg_humidity = [int(i) for i in avg_humidity]

    avg_maxtemp = sum(max_l)/len(max_l)
    print("Highest Average:  ", "%.1f" % avg_maxtemp, "C")

    avg_mintemp = sum(min_l)/len(min_l)
    print("Lowest Average:  ", "%.1f" % avg_mintemp, "C")

    avg_avghumidity = sum(avg_humidity)/len(avg_humidity)
    print("Average Humidity:  ", "%.1f" % avg_avghumidity, "%")


def get_barcharts(answer):
    max_l = list(filter(None, answer.get("Max TemperatureC")))
    max_l = [int(i) for i in max_l]
    min_l = list(filter(None, answer.get("Min TemperatureC")))
    min_l = [int(i) for i in min_l]
    rcolor = colored('+', 'red')
    bcolor = colored('+', 'cyan')
    line_num = 1
    for maxtemp, mintemp in zip(max_l, min_l):
        print("{0:0=2d}".format(line_num), " ", end="")
        cprint(rcolor * maxtemp, end="")
        print(" ", "%2s" % maxtemp, "C")
        print("{0:0=2d}".format(line_num), " ", end="")
        cprint(bcolor * mintemp, end="")
        print(" ", "%2s" % maxtemp, "C")
        line_num = line_num + 1


def get_concatenated_barcharts(answer):
    rcolor = colored('+', 'red')
    bcolor = colored('+', 'cyan')
    line_num = 1
    max_l = list(filter(None, answer.get("Max TemperatureC")))
    max_l = [int(i) for i in max_l]
    min_l = list(filter(None, answer.get("Min TemperatureC")))
    min_l = [int(i) for i in min_l]
    for maxtemp, mintemp in zip(max_l, min_l):
        print("{0:0=2d}".format(line_num), " ", end="")
        cprint(bcolor * mintemp, end="")
        cprint(rcolor * maxtemp, end="")
        print(" ", "%2s" % mintemp, "C", end="")
        print(" - ", "%2s" % maxtemp, "C")
        line_num = line_num + 1

###################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str)
    parser.add_argument('-a', type=str)
    parser.add_argument('-e', type=str)
    parser.add_argument('d', type=str, help='directory')
    arg = parser.parse_args()

    if arg.e:
        fnames_e = renaming_and_conversion(arg.e, '-e', arg.d)
        get_weather_by_year(fnames_e)

    elif arg.a:
        fnames_a = renaming_and_conversion(arg.a, '-a', arg.d)
        answer_a = readf_content(arg.d, fnames_a)
        get_weather_by_month(answer_a)

    elif arg.c:
        fnames_c = renaming_and_conversion(arg.c, '-c', arg.d)
        answer_c = readf_content(arg.d, fnames_c)
        get_barcharts(answer_c)
        get_concatenated_barcharts(answer_c)
