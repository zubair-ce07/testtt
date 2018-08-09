from operator import itemgetter

from helpers.core.calculator_helper import *
from models.calculated_result import CalculatedResult
from models.weather_data import WeatherData


class Calculator:

    def __init__(self, command):
        # get data populated in WeatherData model and then calculate
        self.data = WeatherData.get_data()
        self.__calculate(command)

    def __calculate(self, command):
        print()
        try:
            for entry in command:

                if entry == "-e":

                    # for command -e show yearly MIN/MAX temperatures & Max humidity
                    # input format "-e 2013"
                    index = command.index(entry)
                    arg = command[index + 1]  # getting entered year
                    max_temp_list = []

                    # appending entries of all months of year in one list
                    # for sorting later
                    for key, value in self.data[arg].items():
                        max_temp_list = max_temp_list + value

                    data = list()
                    sorted_arr = sorted(max_temp_list, key=itemgetter('max_temperature_c'))
                    data.append({'date': sorted_arr.pop()['pkt'], 'value': str(sorted_arr.pop()['max_temperature_c']),
                                 'text': 'Highest:', 'ending': ''})
                    sorted_arr = sorted(max_temp_list, key=itemgetter('min_temperature_c'))
                    data.append({'date': sorted_arr.pop()['pkt'], 'value': str(sorted_arr.pop()['min_temperature_c']),
                                 'text': 'Lowest:', 'ending': ''})
                    sorted_arr = sorted(max_temp_list, key=itemgetter('max_humidity'))
                    data.append({'date': sorted_arr.pop()['pkt'], 'value': str(sorted_arr.pop()['max_humidity']),
                                 'text': 'Humidity:', 'ending': '%'})

                    # saving calculated results
                    CalculatedResult.save_results(entry, data)

                elif entry == "-a" or entry == "-c" or entry == "-d":

                    # input format "-a 2013/6"  "-c 2013/6"  "-d 2013/6"
                    index = command.index(entry)
                    arg = command[index + 1]
                    # for given year of month 2012/6
                    year, month = arg.split('/')[0], month_with_num(arg.split('/')[1])
                    if month is None:
                        raise ValueError()

                    if entry == "-a":

                        # command -a for specific month show highest avg, lowest avg and avg mean humidity
                        avg_high_temp = cal_average(find_keys_in_arr('max_temperature_c', self.data[year][month]))
                        avg_low_temp = cal_average(find_keys_in_arr('min_temperature_c', self.data[year][month]))
                        avg_most_humid_temp = cal_average(find_keys_in_arr('mean_humidity', self.data[year][month]))

                        data = list()
                        data.append({'text': 'Highest Average', 'value': str(avg_high_temp), 'ending': ''})
                        data.append({'text': 'Lowest Average', 'value': str(avg_low_temp), 'ending': ''})
                        data.append({'text': 'Average Mean Humidity', 'value': str(avg_most_humid_temp), 'ending': '%'})

                        # saving calculated results
                        CalculatedResult.save_results(entry, data)

                    elif entry == "-c" or entry == "-d":

                        # command -c print 2 lines of + in different colors
                        # command -d print 1 + line of + in mixed colors
                        index = command.index(entry)
                        arg = command[index + 1]
                        # for given year of month 2012/6
                        year, month = arg.split('/')[0], month_with_num(arg.split('/')[1])
                        if month is None:
                            raise ValueError()

                        data = list()
                        data.append({'text': year + " " + month, 'value': self.data[year][month]})
                        CalculatedResult.save_results(entry, data)
        except ValueError as ve:
            print("got value error! {0}".format(ve))
            return
        except IndexError as ie:
            print("got index error! {0}".format(ie))
            return
        except KeyError as ke:
            print("got key error! {0}".format(ke))
            print("for years try", WeatherData.get_years())
            return
