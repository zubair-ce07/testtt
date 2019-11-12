import sys
import os
from os import system
from datetime import datetime
import calendar
import statistics
from termcolor import colored


def generate_report(parsed_list, info_type):
    system('clear')
    if info_type == '-e':
        max_temp = max([mt.max_temprature
                        for mt in parsed_list])
        lowest_temp = max(lt.lowest_temprature
                          for lt in parsed_list)
        most_humid = max(mh.most_humid for mh in parsed_list)
        print("\t\t\t\t*** RESULTS OF THE YEAR ***")
        max_temp_date = [mt.date for mt in parsed_list
                         if mt.max_temprature is max_temp][0].split('-')
        print("""\t\t\t\tHighest: {}C on {} {}""".format(max_temp,
                                   calendar.month_name[int(max_temp_date[1])],
                                   max_temp_date[2]))
        lowest_temp_date = [ltd.date for ltd in parsed_list
                            if ltd.lowest_temprature is lowest_temp][0].split('-')
        print("\t\t\t\tLowest: {}C on {} {}".format(lowest_temp,
                                                calendar.month_name[int(lowest_temp_date[1])],
                                                lowest_temp_date[2]))
        most_humid_date = [mh.date for mh in parsed_list
        if mh.most_humid is most_humid][0].split('-')
        print("\t\t\t\tHumid: {}% on {} {}".format(most_humid,
                                            calendar.month_name[int(most_humid_date[1])],
                                            most_humid_date[2]))
    elif info_type == '-a':
        print("\t\t\t\t*** RESULTS OF THE MONTH ***")
        print("\t\t\t\tHighest Average: {}C".format(int(statistics.mean([mt.max_temprature
                                                    for mt in parsed_list]))))
        print("\t\t\t\tLowest Average: {}C"
        .format(int(statistics.mean(lt.lowest_temprature
                                    for lt in parsed_list))))
        print("\t\t\t\tAverage Humidity: {}%".format(int(statistics.mean(mh.most_humid
                                                    for mh in parsed_list))))
    elif info_type == '-c' or info_type == '-d':
        max_temprature_bar = ''
        lowest_temprature_bar = ''
        print("\t\t\t\t*** HORIZONTAL BAR CHART RESULTS OF THE MONTH ***")
        print("\n{} {}".format(calendar.month_name[int(parsed_list[0].date.split("-")[1])],
                                parsed_list[0].date.split("-")[0]))
        for value in parsed_list:
            for mt in range(value.max_temprature):
                max_temprature_bar += '+'
            for mt in range(value.lowest_temprature):
                lowest_temprature_bar += '+'
            if info_type == '-c':
                print("{} {} {}C".format(str(value.date.split('-')[2]).zfill(2),
                                            colored(max_temprature_bar, 'red'),
                                             value.max_temprature))
                print("{} {} {}C".format(str(value.date.split('-')[2]).zfill(2),
                                            colored(lowest_temprature_bar, 'blue'),
                                             value.lowest_temprature))
            if info_type == '-d':
                print("{} {}{} {}C - {}C".format(str(value.date.split('-')[2]).zfill(2),
                                                colored(lowest_temprature_bar, 'blue'),
                                                 colored(max_temprature_bar, 'red'),
                                                 value.lowest_temprature, value.max_temprature))
            max_temprature_bar = ''
            lowest_temprature_bar = ''
