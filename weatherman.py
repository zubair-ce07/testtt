import calendar
import sys
import os
from termcolor import colored, cprint


class Table:
   
    def __init__(self, headings=None):
        self.rows = []
        self.headings = []
        self.set_headings(headings)

    def add_row(self, row):
        self.rows.append(row)

    def set_headings(self, headings):
        self.headings = headings

    def print_table(self):
        print(self.headings)
        for row in self.rows:
            print(row)


class Parser:
    file_name = ""

    def __init__(self, file_name):
        self.weather_reading = Table()
        self.file_name = file_name
        if(not(self.file_name.endswith(".txt"))):
            self.file_name = self.file_name + ".txt"
        self.set_weather_reading()

    def type_converstion(self, data):
        data_type = ['string', 'int', 'int', 'int', 'int', 'int', 'int',
                     'int', 'int', 'int', 'int', 'int', 'int', 'float',
                     'float', 'float', 'int', 'int', 'int', 'float',
                     'int', 'string', 'int']

        type_map = {'string': str, 'int': int, 'float': float}
        results = [type_map[t](d or 0) for t, d in zip(data_type, data)]
        return results

    def set_weather_reading(self):
        f = open(self.file_name, "r")
        heading = f.readline().split(',')
        heading = [i.strip() for i in heading]
        self.weather_reading.set_headings(heading)

        while True:
            day_readings = f.readline().split(',')
            if len(day_readings) == 1:
                break
            day_readings = [i.strip() for i in day_readings]
            day_readings = self.type_converstion(day_readings)
            self.weather_reading.add_row(day_readings)


class Results:
    def __init__(self):
        self.highest_temperature_monthly = []
        self.lowest_temperature_monthly = []
        self.highest_temperature = 0
        self.lowest_temperature = 0
        self.highest_humidity = 0

        self.average_highest_temperature = 0
        self.average_lowest_temperature = 0
        self.average_humidity = 0


class CalculateReadings:

    def __init__(self, file_name):
        self.parser = Parser(file_name)
        self.results = Results()

    def cal_highest_average_monthly(self):
        for row in self.parser.weather_reading.rows:
            self.results.average_highest_temperature += row[1]

        self.results.average_highest_temperature\
            /= len(self.parser.weather_reading.rows)

        return self.results.average_highest_temperature

    def cal_lowest_average_monthly(self):
        for row in self.parser.weather_reading.rows:
            self.results.average_lowest_temperature += row[3]

        self.results.average_lowest_temperature \
            /= len(self.parser.weather_reading.rows)

        return self.results.average_lowest_temperature

    def cal_average_mean_humidity_monthly(self):
        for row in self.parser.weather_reading.rows:
            self.results.average_humidity += row[8]

        self.results.average_humidity \
            /= len(self.parser.weather_reading.rows)

        return self.results.average_humidity

    def set_highest_lowest_temperature_monthly(self):
        for index in range(len(self.parser.weather_reading.rows)):
            self.results.highest_temperature_monthly.\
                append(self.parser.weather_reading.rows[index][1])
            self.results.lowest_temperature_monthly.\
                append(self.parser.weather_reading.rows[index][3])
    
    def print_highest_lowest_temperature_monthly(self):
        for index in range(len(self.results.highest_temperature_monthly)):
            print(index+1, end='')
            for value in range(0, self.results.highest_temperature_monthly[index]):
                cprint('+', 'red', end='')
            print('\n')

            print(index+1, end='')
            for value in range(0, self.results.lowest_temperature_monthly[index]):
                cprint('+', 'blue', end='')
            print('\n')

    def bonus_print_highest_lowest_temperature_monthly(self):
        for index in range(len(self.results.highest_temperature_monthly)):
            print(index+1, end='')
            
            for value in range(0, self.results.lowest_temperature_monthly[index]):
                cprint('+', 'blue', end='')
            
            for value in range(0, self.results.highest_temperature_monthly[index]):
                cprint('+', 'red', end='')

            print(self.results.lowest_temperature_monthly[index], "C-", end='', sep='')
            print(self.results.highest_temperature_monthly[index], "C", sep='')

    def set_highest_temperature(self):
        self.results.highest_temperature = max(l[1] for l in self.parser.weather_reading.rows)
        return self.results.highest_temperature
    
    def set_lowest_temperature(self):
        self.results.lowest_temperature = min(l[3] for l in self.parser.weather_reading.rows)
        return self.results.lowest_temperature
    
    def set_highest_humidity(self):
        self.results.highest_humidity = max(l[7] for l in self.parser.weather_reading.rows)
        return self.results.highest_humidity

    def print_highest_lowest_humidity_month(self):

        self.set_highest_temperature()
        self.set_lowest_temperature()
        self.set_highest_humidity()

        print("Highest: ", self.results.highest_temperature, "C", sep='')
        print("Lowest: ", self.results.lowest_temperature, "C", sep='')
        print("Humidity: ", self.results.highest_humidity, "%", sep='')
        print('\n')


# --------------------------------Main-----------------------------------


argument_list_original = sys.argv
argument_list = []

i = 2

while(True):
    argument_list.append(argument_list_original[0])
    argument_list.append(argument_list_original[1])
    argument_list.append(argument_list_original[i])
    i = i + 1
    argument_list.append(argument_list_original[i])
    i = i + 1

    if(argument_list[2] == '-a'):
        your_directory = argument_list[1]

        month_num = int(argument_list[3].split("/")[-1])
        month = calendar.month_abbr[month_num]

        year = argument_list[3][:4]

        file_name = your_directory+"Murree_weather_" + year+"_"+month

        calculate_readings_obj = CalculateReadings(file_name)

        print("Highest Average:", '%.2f' % calculate_readings_obj.cal_highest_average_monthly(), "C", sep='')
        print("Lowest Average:", '%.2f' % calculate_readings_obj.cal_lowest_average_monthly(), "C", sep='')
        print("Average Mean Humidity:", '%.2f' % calculate_readings_obj.cal_average_mean_humidity_monthly(), "%", sep='')

    if(argument_list[2] == '-c'):
        your_directory = argument_list[1]

        month_num = int(argument_list[3].split("/")[-1])
        month = calendar.month_abbr[month_num]

        year = argument_list[3][:4]

        file_name = your_directory+"Murree_weather_" + year+"_"+month

        calculate_readings_obj = CalculateReadings(file_name)

        calculate_readings_obj.set_highest_lowest_temperature_monthly()
        calculate_readings_obj.bonus_print_highest_lowest_temperature_monthly()

    if(argument_list[2] == '-e'):
        your_directory = argument_list[1]
        to_find = argument_list[3]
        monthly_data = []
        index = 0
        yearly_highest_temperature = 0
        yearly_lowest_temperature = 999
        yearly_highest_humidity = 0

        for file_name in os.listdir(your_directory):

            if (file_name.find(to_find) != -1):
                monthly_data.append(CalculateReadings(your_directory+'/'+file_name))

                monthly_data[index].set_highest_temperature()
                monthly_data[index].set_lowest_temperature()
                monthly_data[index].set_highest_humidity()

                if(monthly_data[index].results.highest_temperature > yearly_highest_temperature):
                    yearly_highest_temperature = monthly_data[index].results.highest_temperature
                if(monthly_data[index].results.lowest_temperature < yearly_lowest_temperature):
                    yearly_lowest_temperature = monthly_data[index].results.lowest_temperature
                if(monthly_data[index].results.highest_humidity > yearly_highest_humidity):
                    yearly_highest_humidity = monthly_data[index].results.highest_humidity

                index = index+1

        print("Highest: ", yearly_highest_temperature, "C", sep='')
        print("Lowest: ", yearly_lowest_temperature, "C", sep='')
        print("Humidity: ", yearly_highest_humidity, "%", sep='')

    argument_list.clear()
    if(i == 8 or len(argument_list_original) < 7):
        break
