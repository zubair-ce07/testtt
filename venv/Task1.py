# Task-1
from datetime import datetime
import numpy
import glob
import operator
import sys
import re


# data structure for collecting weather data
class WeatherData:

    def __init__(self):
        self.pkt = 0,
        self.max_temperatureC = 0,
        self.mean_temperatureC = 0,
        self.min_temperatureC = 0,
        self.dew_pointC = 0,
        self.mean_dew_pointC = 0,
        self.min_dew_pointC = 0,
        self.max_humidity = 0,
        self.mean_humidity = 0,
        self.min_humidity = 0,
        self.max_sea_level_pressureh_Pa = 0,
        self.mean_sea_level_pressureh_Pa = 0,
        self.min_sea_level_pressureh_Pa = 0,
        self.max_visibility_Km = 0,
        self.mean_visibility_Km = 0,
        self.min_visibility_KM = 0,
        self.max_wind_speed_Kmh = 0,
        self.mean_wind_speed_Kmh = 0,
        self.max_gust_speed_Kmh = 0,
        self.precipitation_mm = 0,
        self.cloud_cover = 0,
        self.events = 0,
        self.wind_dir_degrees = 0


# data structure for holding the calculations results.
class CalResults:

    def __init__(self):
        self.highest_temperature = 0.0,
        self.highest_temperature_date = 0,
        self.lowest_temperature = 0.0,
        self.lowest_temperature_date = 0,
        self.max_humidity = 0.0
        self.max_humidity_date = 0,
        self.avg_high_temp = 0,
        self.low_avg_temp = 0,
        self.avg_mean_humidity = 0


# class for computing the calculations given the readings data structure.
class ComputingSubTaskResults:
    def high_low_temp_and_day(self, files_yearly_parameter):
        save_high_temp_data = []
        save_low_temp_data = []
        save_humid_data = []
        data = {}
        result_data = CalResults()

        for a in files_yearly_parameter:
            if a is not None:

                for b in a:
                    if b is not None:

                        if b.max_temperatureC != '':
                            save_high_temp_data.append(int(b.max_temperatureC))
                            data[b.max_temperatureC] = b.pkt

                        if b.min_temperatureC != '':
                            save_low_temp_data.append(int(b.min_temperatureC))
                            data[b.min_temperatureC] = b.pkt

                        if b.max_humidity != '':
                            save_humid_data.append(int(b.max_humidity))
                            data[b.max_humidity] = b.pkt

        if save_high_temp_data.__len__():
            result_data.highest_temperature = max(save_high_temp_data)
            result_data.highest_temperature_date = data.get('%s' % result_data.highest_temperature)

        if save_low_temp_data.__len__():
            result_data.lowest_temperature = min(save_low_temp_data)
            result_data.lowest_temperature_date = data.get('%s' % result_data.lowest_temperature)

        if save_humid_data.__len__():
            result_data.max_humidity = max(save_humid_data)
            result_data.max_humidity_date = data.get('%s' % result_data.max_humidity)

        # high_date_converted = datetime.strptime(data.get('%s' % result_data.highest_temperature), '%Y-%m-%d')
        high_date_converted = datetime.strptime(result_data.highest_temperature_date, '%Y-%m-%d')
        # low_date_converted = datetime.strptime(data.get('%s' % result_data.lowest_temperature), '%Y-%m-%d')
        low_date_converted = datetime.strptime(result_data.lowest_temperature_date, '%Y-%m-%d')
        # humid_date_converted = datetime.strptime(data.get('%s' % result_data.max_humidity), '%Y-%m-%d')
        humid_date_converted = datetime.strptime(result_data.max_humidity_date, '%Y-%m-%d')

        print('\nHighest: %sC on %s %d' % (result_data.highest_temperature, high_date_converted.strftime("%B"),
                                           high_date_converted.day))
        print('Lowest: %sC on %s %d' % (result_data.lowest_temperature, low_date_converted.strftime("%B"),
                                        low_date_converted.day))
        print('Humidity: %s%% on %s %d' % (result_data.max_humidity, humid_date_converted.strftime("%B"),
                                           humid_date_converted.day))

    # def low_temp_day(self, files_yearly_parameter):
    #     save_temp_data = []
    #     data = {}
    #     result_data = CalResults()
    #
    #     for a in files_yearly_parameter:
    #         if a is not None:
    #
    #             for b in a:
    #                 if b is not None:
    #
    #                     if b.min_temperatureC != '':
    #                         save_temp_data.append(int(b.min_temperatureC))
    #                         data[b.min_temperatureC] = b.pkt
    #
    #     if save_temp_data.__len__() > 0:
    #         result_data.lowest_temperature = min(save_temp_data)
    #         result_data.lowest_temperature_date = data.get('%s' % result_data.lowest_temperature)
    #
    #         date_converted = datetime.strptime(data.get('%s' % result_data.lowest_temperature), '%Y-%m-%d')
    #         month_converted = date_converted.strftime("%B")
    #         day_converted = date_converted.day
    #
    #         print('Lowest: %sC on %s %d' % (result_data.lowest_temperature, month_converted, day_converted))
    #     else:
    #         print('Lowest: %sC on %s %d' % (0, 0, 0))

    # def humidity_and_day(self, files_yearly_parameter):
    #     save_temp_data = []
    #     data = {}
    #     result_data = CalResults()
    #
    #     for a in files_yearly_parameter:
    #         if a is not None:
    #
    #             for b in a:
    #                 if b is not None:
    #
    #                     if b.max_humidity != '':
    #                         save_temp_data.append(int(b.max_humidity))
    #                         data[b.max_humidity] = b.pkt
    #
    #     if save_temp_data.__len__() > 0:
    #         result_data.max_humidity = max(save_temp_data)
    #         result_data.max_humidity_date = data.get('%s' % result_data.max_humidity)
    #
    #         date_converted = datetime.strptime(data.get('%s' % result_data.max_humidity), '%Y-%m-%d')
    #         month_converted = date_converted.strftime("%B")
    #         day_converted = date_converted.day
    #
    #         print('Humidity: %s%% on %s %d' % (result_data.max_humidity, month_converted, day_converted))
    #     else:
    #         print('Humidity: %s%% on %s %d' % (0, 0, 0))

    def avg_high_temp(self, files_yearly_parameter):
        high_temp_data = []
        low_temp_data = []
        mean_humidity_date = []
        result_data = CalResults()

        for a in files_yearly_parameter:
            if a is not None:

                for b in a:
                    if b is not None:

                        if b.max_temperatureC != '':
                            high_temp_data.append(int(b.max_temperatureC))

                        if b.min_temperatureC != '':
                            low_temp_data.append(int(b.min_temperatureC))

                        if b.mean_humidity != '':
                            mean_humidity_date.append(int(b.mean_humidity))

        if high_temp_data.__len__():
            # max_value = int(sum(high_temp_data) / high_temp_data.__len__())
            result_data.avg_high_temp = int(sum(high_temp_data) / high_temp_data.__len__())

        if low_temp_data.__len__():
            # min_value = int(sum(low_temp_data) / low_temp_data.__len__())
            result_data.low_avg_temp = int(sum(low_temp_data) / low_temp_data.__len__())

        if mean_humidity_date.__len__():
            # mean_value = int(sum(mean_humidity_date) / mean_humidity_date.__len__())
            result_data.avg_mean_humidity = int(sum(mean_humidity_date) / mean_humidity_date.__len__())

        print('\nHighest Average: %sC' % result_data.avg_high_temp)
        print('Lowest Average: %sC' % result_data.low_avg_temp)
        print('Average Mean Humidity: %s%%' % result_data.avg_mean_humidity)

    def chart_horizontal(self, files_yearly_parameter):
        for a in files_yearly_parameter:
            if a is not None:

                for b in a:
                    if b is not None:

                        if b.max_temperatureC != '':
                            self.draw_chart_horizontal(b.max_temperatureC, '31', b.pkt)

                            if b.min_temperatureC != '':
                                self.draw_chart_horizontal(b.min_temperatureC, '34', b.pkt)
                            else:
                                self.draw_chart_horizontal(0, '34', b.pkt)
                        else:
                            self.draw_chart_horizontal(0, '31', b.pkt)
                            if b.min_temperatureC != '':
                                self.draw_chart_horizontal(b.min_temperatureC, '34', b.pkt)
                            else:
                                self.draw_chart_horizontal(0, '34', b.pkt)

    def double_chart_horizontal(self, files_yearly_parameter):
        high_temp_data = 0
        low_temp_data = 0
        for a in files_yearly_parameter:
            if a is not None:

                for b in a:
                    if b is not None:

                        if b.max_temperatureC != '':
                            high_temp_data = b.max_temperatureC

                        if b.min_temperatureC != '':
                            low_temp_data = b.min_temperatureC

                        self.draw_double_chart_horizontal(low_temp_data, high_temp_data, 34, 31, b.pkt)

    def draw_chart_horizontal(self, count, color, date_value):
        count = int(count)
        print("\033[%d;10m%s " % (37, date_value[7:]), end='')

        for i in range(count):
            print("\033[%d;10m+" % int(color), end='')

        print("\033[%d;10m %sC" % (37, count))

    def draw_double_chart_horizontal(self, mincount, maxcount, mincolor, maxcolor, date_value):
        mincount = int(mincount)
        maxcount = int(maxcount)

        print("\033[%d;10m%s " % (37, date_value[7:]), end='')
        for i in range(mincount):
            print("\033[%d;10m+" % int(mincolor), end='')
        for b in range(maxcount):
            print("\033[%d;10m+" % int(maxcolor), end='')

        print("\033[%d;10m %sC-%sC" % (37, mincount, maxcount))


# reading data from files
class ReadData:
    def read_data(self, path):
        # Open file and read Data
        # file = open("/home/abdullah/theLab/weatherfiles/weatherfiles/Murree_weather_2004_Aug.txt", "r")
        file = open(path, "r")
        weather_instances = numpy.ndarray((32,), dtype=numpy.object)

        # Ignore header
        next(file)
        i = 0
        for f in file.readlines():
            weather_instances[i] = WeatherData()
            # f = file.read()
            if f is not None:
                weather_data_values = []
                weather_data_values = f.split(",")
                weather_instances[i].pkt = weather_data_values[0]
                weather_instances[i].max_temperatureC = weather_data_values[1]
                weather_instances[i].mean_temperatureC = weather_data_values[2]
                weather_instances[i].min_temperatureC = weather_data_values[3]
                weather_instances[i].dew_pointC = weather_data_values[4]
                weather_instances[i].mean_dew_pointC = weather_data_values[5]
                weather_instances[i].min_dew_pointC = weather_data_values[6]
                weather_instances[i].max_humidity = weather_data_values[7]
                weather_instances[i].mean_humidity = weather_data_values[8]
                weather_instances[i].min_humidity = weather_data_values[9]
                weather_instances[i].max_sea_level_pressureh_Pa = weather_data_values[10]
                weather_instances[i].mean_sea_level_pressureh_Pa = weather_data_values[11]
                weather_instances[i].min_sea_level_pressureh_Pa = weather_data_values[12]
                weather_instances[i].max_visibility_Km = weather_data_values[13]
                weather_instances[i].mean_visibility_Km = weather_data_values[14]
                weather_instances[i].min_visibility_KM = weather_data_values[15]
                weather_instances[i].max_wind_speed_Kmh = weather_data_values[16]
                weather_instances[i].mean_wind_speed_Kmh = weather_data_values[17]
                weather_instances[i].max_gust_speed_Kmh = weather_data_values[18]
                weather_instances[i].precipitation_mm = weather_data_values[19]
                weather_instances[i].cloud_cover = weather_data_values[20]
                weather_instances[i].events = weather_data_values[21]
                weather_instances[i].wind_dir_degrees = weather_data_values[22]

                i += 1

        # filter(None, weather_instances)
        return weather_instances

    def read_data_yearly(self, year):
        read_again = ReadData()
        # files_yearly = numpy.ndarray((7,), dtype=numpy.object)
        files_count = 0
        read_requested_data = glob.glob('/home/abdullah/theLab/weatherfiles/weatherfiles/*%s*.txt' % year)
        files_yearly = numpy.ndarray((read_requested_data.__len__(),), dtype=numpy.object)

        for file_name in read_requested_data:
            temp = numpy.ndarray((1,), dtype=numpy.object)
            temp = read_again.read_data(file_name)

            if temp is not None:
                files_yearly[files_count] = read_again.read_data(file_name)
                files_count += 1

        return files_yearly

    def read_data_monthly(self,year, month):
        read_again = ReadData()
        # files_yearly = numpy.ndarray((7,), dtype=numpy.object)
        files_count = 0
        read_requested_data = glob.glob('/home/abdullah/theLab/weatherfiles/weatherfiles/*%s*%s**.txt' % (year, month))
        files_yearly = numpy.ndarray((read_requested_data.__len__(),), dtype=numpy.object)

        for file_name in read_requested_data:
            temp = numpy.ndarray((1,), dtype=numpy.object)
            temp = read_again.read_data(file_name)

            if temp is not None:
                files_yearly[files_count] = read_again.read_data(file_name)
                files_count += 1

        return files_yearly


# creating the reports given the results data structure.
class Reports:
    # Calculates high temp & day, low temp and day
    # and most humidity and day
    def fetch_high_low_temp_humidity_day(self, year):
        read_data_object = ReadData()
        files_yearly = read_data_object.read_data_yearly(year)

        hightemp = ComputingSubTaskResults()
        hightemp.high_low_temp_and_day(files_yearly)
        # hightemp.low_temp_day(files_yearly)
        # hightemp.humidity_and_day(files_yearly)

    # Calculates avg high temp, avg low temp
    # and avg mean humidity
    def fetch_avg(self, year, month):
        read_data_object = ReadData()
        files_yearly = read_data_object.read_data_monthly(year, month)

        hightemp = ComputingSubTaskResults()
        hightemp.avg_high_temp(files_yearly)

    # 3. for month draw horizontal bar charts on the console for the highest and lowest temperature on each day.
    # Highest in red and lowest in blue.
    def draw_high_low_charts(self, year, month):
        read_data_object = ReadData()
        files_yearly = read_data_object.read_data_monthly(year, month)

        hightemp = ComputingSubTaskResults()
        hightemp.chart_horizontal(files_yearly)
        hightemp.double_chart_horizontal(files_yearly)

    # 4. Multiple Reports
    # def fetch_multiple_reports(self,year_month):
    def multiple_reports(self ,x_arguments):
        if len(x_arguments) > 3:
            i = 1
            while i < len(x_arguments):
                get_result = SubMain().validate_input(x_arguments[i+1])
                if get_result:
                    SubMain().switch_value(x_arguments[i], x_arguments[i+1])
                else:
                    print("\n%s Value is not in correct format!\n" % x_arguments[i+1])
                i += 2

    # # 5. Bonus Task
    # def draw_mix_chart(self, year, month):
    #     read_data_object = ReadData()
    #     files_yearly = read_data_object.read_data_monthly(year, month)
    #
    #     hightemp = ComputingSubTaskResults()
    #     hightemp.double_chart_horizontal(files_yearly)


# For Tasks division
class SubMain:

    def sub_task_1(self, year_value):
            #print("\nEnter Year : ")
            year_value = year_value
            read_reports = Reports()
            read_reports.fetch_high_low_temp_humidity_day(year_value)

    def sub_task_2(self, year_month_value):
        # print("\nEnter Year/month : ")
        year_value = year_month_value

        read_reports = Reports()
        month_value = year_value
        month_value_split = month_value.split("/")

        int_to_month = month_value_split[1]
        date_converted = datetime.strptime(int_to_month, '%m')
        month_converted = date_converted.strftime("%b")

        read_reports.fetch_avg(month_value_split[0], month_converted)

    def sub_task_3(self, year_month_value):
        year_value = year_month_value

        read_reports = Reports()
        month_value = year_value
        month_value_split = month_value.split("/")

        int_to_month = month_value_split[1]
        date_converted = datetime.strptime(int_to_month, '%m')
        month_converted_cap = date_converted.strftime("%B")

        month_converted = date_converted.strftime("%b")

        print("\n%s %s" % (month_converted_cap, month_value_split[0]))

        read_reports.draw_high_low_charts(month_value_split[0], month_converted)

    def sub_task_4(self, x_arguments):
        read_reports = Reports()
        read_reports.multiple_reports(x_arguments)

    # def sub_task_5(self):
    #     # while True:
    #     print("\nEnter Year/month : ")
    #     year_value = "2005/8"# input()
    #
    #     read_reports = Reports()
    #     month_value = year_value
    #     month_value_split = month_value.split("/")
    #
    #     int_to_month = month_value_split[1]
    #     date_converted = datetime.strptime(int_to_month, '%m')
    #     month_converted_cap = date_converted.strftime("%B")
    #
    #     month_converted = date_converted.strftime("%b")
    #
    #     print("%s %s" % (month_converted_cap, month_value_split[0]))
    #
    #     read_reports.draw_mix_chart(month_value_split[0], month_converted)

    def switch_value(self, read_arguments, argument_value):
        if read_arguments == '-e':
            self.sub_task_1(argument_value)
        if read_arguments == '-a':
            self.sub_task_2(argument_value)
        if read_arguments == '-c':
            self.sub_task_3(argument_value)

    def validate_input(self, to_validate):

        result = re.match("(20[0-1][0-9])|[//](1[0-2]|0[1-9]|\d)", to_validate)
        return result


# Main
class Main:
    print('Number of arguments:', len(sys.argv), 'arguments.')
    arguments = []
    arguments = list(sys.argv)
    print('Argument List:', str(sys.argv))
    # task_no = input()
    if len(arguments) < 4:
        bool_result = SubMain().validate_input(arguments[2])
        if bool_result:
            SubMain().switch_value(arugments[1], arguments[2])
        else:
            print("input not correct! ")
    else:
        SubMain().sub_task_4(arguments)

