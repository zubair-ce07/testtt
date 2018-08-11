"""
This module read user input , read files , perform calculation and generate reports
"""
from datetime import datetime
import argparse
import os
import calendar


class WeatherReading:
    """The class holds weather data for single day"""
    highest_temp = 0
    lowest_temp = 0
    most_humidity = 0
    mean_humidity = 0
    date = ''

    def add_month_value(self, highest_tmp, lowest_tmp, most_humidity, mean_humidity, date):
        """The method stores data for single day"""
        self.highest_temp = highest_tmp
        self.lowest_temp = lowest_tmp
        self.most_humidity = most_humidity
        self.mean_humidity = mean_humidity
        self.date = date

    def view_day_data(self):
        """The method print data for single day"""
        print('date:', self.date)
        print('Max temp:', self.highest_temp)
        print('Min temp:', self.lowest_temp)
        print('Most humidity:', self.most_humidity)
        print('Mean humidity:', self.mean_humidity)


class WeatherResults:
    """The class holds calculated weather results"""
    maximum_temp_value = 0
    minimum_temp_value = 0
    most_humidity_value = 0
    max_temp_date = ''
    min_temp_date = ''
    most_humidity_date = ''
    average_maximum_temp = 0
    average_minimum_temp = 0
    average_mean_humidity = 0

    def set_weather_results_yearly(
            self, max_tmp, max_temp_date, min_tmp,
            min_temp_date, most_humidity_val, most_humidity_date):
        """The method stores maximum and minimum temperature for every single day"""
        self.maximum_temp_value = max_tmp
        self.minimum_temp_value = min_tmp
        self.most_humidity_value = most_humidity_val
        self.max_temp_date = max_temp_date
        self.min_temp_date = min_temp_date
        self.most_humidity_date = most_humidity_date

    def set_weather_results_averages(self, avrg_max, avrg_min, avrg_mean_humid):
        """The method populate the average temperature of a month"""
        self.average_maximum_temp = avrg_max
        self.average_minimum_temp = avrg_min
        self.average_mean_humidity = avrg_mean_humid


class Report:
    """The class hold the results of temperaures"""
    DATE_FORMAT = '%Y-%m-%d'
    MONTH_DAY_FORMAT = '%B %d'
    MONTH_YEAR_FORMAT = '%B %Y'

    def year_report(self, results):
        """The method prints the report of year maximun, minimum temperature and most humidity"""
        date_format = datetime.strptime(
            results.max_temp_date, self.DATE_FORMAT)
        print(
            'Maximum: ', results.maximum_temp_value, 'C',
            'on ', datetime.strftime(date_format, self.MONTH_DAY_FORMAT))
        date_format = datetime.strptime(
            results.min_temp_date, self.DATE_FORMAT)
        print(
            'Lowest: ', results.minimum_temp_value, 'C',
            'on ', datetime.strftime(date_format, self.MONTH_DAY_FORMAT))
        date_format = datetime.strptime(
            results.most_humidity_date, self.DATE_FORMAT)
        print(
            'Humidity: ', results.most_humidity_value, '%',
            'on ', datetime.strftime(date_format, self.MONTH_DAY_FORMAT))

    def month_average_report(self, results):
        """The method prints averages of (max min temperature,mean humidity)"""
        print('Highest Average: ', results.average_maximum_temp, 'C')
        print('Lowest Average: ', results.average_minimum_temp, 'C')
        print('Average Mean Humidity: ',
              results.average_mean_humidity, '%')

    def graphic_report(self, month_year, day_data_obj):
        """The method prints the graphic report of month max min temperature"""
        date_format = datetime.strptime(month_year, self.DATE_FORMAT)
        print(
            datetime.strftime(date_format, self.MONTH_YEAR_FORMAT))
        for day_num, day_data in enumerate(day_data_obj):
            if day_data.highest_temp == '' or day_data.lowest_temp == '':
                print(day_num + 1, 'N/A')
                print(day_num + 1, 'N/A')
            else:
                highest_temp_value = int(day_data.highest_temp)
                lowest_temp_value = int(day_data.lowest_temp)
                total_characters_max_temp = '+' * highest_temp_value
                print("{} {} {} {} {} C".format(
                    day_num + 1, '\033[1;31m', total_characters_max_temp,
                    '\033[1;m', highest_temp_value))
                total_characters_min_temp = '+' * lowest_temp_value
                print("{} {} {} {} {} C".format(
                    day_num + 1, '\033[1;34m', total_characters_min_temp,
                    '\033[1;m', lowest_temp_value))
        print()
        print('BONUS TASK')
        print(
            datetime.strftime(date_format, self.MONTH_YEAR_FORMAT))
        for day_num, day_data in enumerate(day_data_obj):
            if day_data.highest_temp == ''or day_data.lowest_temp == '':
                print(day_num + 1, 'N/A')
            else:
                highest_temp_value = int(day_data.highest_temp)
                lowest_temp_value = int(day_data.lowest_temp)
                total_characters_max_temp = '+' * highest_temp_value
                total_characters_min_temp = '+' * lowest_temp_value
                print("{} {} {} {} {} {} {} {} C - {} C".format(day_num + 1,\
                        '\033[1;34m', total_characters_min_temp,\
                        '\033[1;m', '\033[1;31m', total_characters_max_temp,\
                        '\033[1;m', lowest_temp_value, highest_temp_value))


class DataCalculation:
    """The class performs calculations on weather readings"""

    def calculate_yearly_month_max(self, day_data_obj):
        """The method find maximum,minimum temperature and most humidity"""
        max_temp = 0
        max_temp_date = ''
        min_temp = 0
        min_temp_date = ''
        most_humidity1 = 0
        most_humidity_date = ''
        max_temp = max([int(day_data_obj[i].highest_temp) for i in range(
            len(day_data_obj)) if day_data_obj[i].highest_temp != ''])
        min_temp_list = [int(day_data_obj[i].lowest_temp) for i in range(
            len(day_data_obj)) if day_data_obj[i].lowest_temp != '']
        min_temp = min(min_temp_list)
        most_humidity_list = [int(day_data_obj[i].most_humidity) for i in range(
            len(day_data_obj)) if day_data_obj[i].most_humidity != '']
        most_humidity1 = max(most_humidity_list)
        date_list = [[day_data_obj[i].date for i in range(len(day_data_obj))
                      if day_data_obj[i].date != ''
                      if day_data_obj[i].highest_temp != ''], [int(day_data_obj[i].highest_temp)
                                                               for i in range(len(day_data_obj))
                                                               if day_data_obj[i].highest_temp
                                                               != '']]

        max_value_dates = [[date_list[0][i] for i in range(len(date_list[0])) if date_list[1][i]
                            == max_temp],
                           [date_list[0][i] for i in range(len(date_list[0]))
                            if min_temp_list[i] == min_temp],
                           [date_list[0][i] for i in range(len(date_list[0]))
                            if most_humidity_list[i]
                            == most_humidity1]]
        max_temp_date = str(max_value_dates[0][0])
        min_temp_date = str(max_value_dates[1][0])
        most_humidity_date = str(max_value_dates[2][0])
        return max_temp, max_temp_date, min_temp, min_temp_date, most_humidity1, most_humidity_date

    def calculate_averages(self, day_data_obj):
        """The method calculate averages of maximum,minimum temperature and mean humidity"""
        sum_max_temp = 0
        avrg_max_tmp = 0
        sum_min_temp = 0
        avrg_min_tmp = 0
        sum_mean_humidity = 0
        avrg_mean_humidity = 0
        data_found_count = 0

        max_temp_list = [day_data[1].highest_temp for day_data in enumerate(
            day_data_obj) if day_data[1].highest_temp != '']
        sum_max_temp = sum(list(map(int, max_temp_list)))
        data_found_count = len(max_temp_list)
        min_temp_list = [day_data[1].lowest_temp for day_data in enumerate(
            day_data_obj) if day_data[1].lowest_temp != '']
        sum_min_temp = sum(list(map(int, min_temp_list)))
        mean_humidity_list = [day_data[1].mean_humidity for day_data in enumerate(
            day_data_obj) if day_data[1].mean_humidity != '']
        sum_mean_humidity = sum(list(map(int, mean_humidity_list)))
        avrg_max_tmp = sum_max_temp / data_found_count
        avrg_min_tmp = sum_min_temp / data_found_count
        avrg_mean_humidity = sum_mean_humidity / data_found_count
        return avrg_max_tmp, avrg_min_tmp, avrg_mean_humidity

    def calculate_max_min(self, day_data_obj):
        """The method populate maximum,minimum temperature of month to report class"""
        month_year = day_data_obj[0].date
        return month_year


class FileParser:
    """The class filters the files and populate data to weather reading class"""

    def read_files(self, year_input, path_to_dir):
        """The method read the files"""
        month_count = 0
        file_name_list = []
        convert_month_to_int = 0
        expr = year_input.find('/') > 0
        month_list = []

        def maintain_file_information(file_name, month_number):
            """The method stores files name and month number in the list"""
            file_name_list.append(file_name)
            month_list.append(month_number)
            return file_name_list, month_list
        if expr is True:
            split_month = year_input.split('/')
            convert_year_to_int = int(split_month[0])
            convert_month_to_int = int(split_month[1])
            year_converted = convert_year_to_int
            total_month_file_count = 1
            file_name = "Murree_weather_" + str(year_converted) + \
                "_" + calendar.month_abbr[convert_month_to_int] + ".txt"

            if os.path.isfile(path_to_dir + file_name):
                month_count = 1
                file_name_list, month_list = maintain_file_information(
                    file_name, convert_month_to_int)
        else:
            year_converted = year_input
            for total_months in range(13):
                file_name = "Murree_weather_" + year_converted + \
                    "_" + calendar.month_abbr[total_months] + ".txt"

                if os.path.isfile(path_to_dir + file_name):
                    month_count = month_count + 1
                    file_name_list, month_list = maintain_file_information(
                        file_name, total_months)
            total_month_file_count = month_count
        count = 0
        count_month_days = 0
        sum_ = 0
        for data_insert in range(total_month_file_count):
            count_month_days = calendar.monthrange(
                int(year_converted), int(month_list[data_insert]))[1]
            sum_ = sum_ + count_month_days
        total_days = sum_
        day_index = 0
        day_data_objects = [None]*total_days

        for i in range(total_days):
            day_data_objects[i] = WeatherReading()
        for data_insert in range(month_count):
            count = 0
            file_get = file_name_list[data_insert]
            path2 = path_to_dir + file_get
            file_data1 = open(path2, "r")
            current_month_data = file_data1.read()
            count = calendar.monthrange(
                int(year_converted), int(month_list[data_insert]))[1]
            for month_num in range(count):
                pro_data = current_month_data.split('\n')
                day_data = pro_data[month_num + 1]
                day_pro_data = day_data.split(',', 9)
                max_tmp_val = 0
                min_tmp_val = 0
                most_humid_val = 0
                mean_humid_val = 0
                date3 = ''
                max_tmp_val = day_pro_data[1]
                min_tmp_val = day_pro_data[3]
                most_humid_val = day_pro_data[7]
                mean_humid_val = day_pro_data[8]
                date3 = day_pro_data[0]
                day_data_objects[day_index].add_month_value(
                    max_tmp_val, min_tmp_val, most_humid_val, mean_humid_val, date3)
                day_index += 1
        return day_data_objects


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", help="enter the year", type=str)
    parser.add_argument("-a", help="enter the year", type=str)
    parser.add_argument("-c", help="enter the year", type=str)
    parser.add_argument("path", help="enter the year", type=str)
    args = parser.parse_args()
    read_file_object = FileParser()
    calculate = DataCalculation()
    result1 = WeatherResults()
    report1 = Report()
    if args.e is not None:
        weather_record = read_file_object.read_files(args.e, args.path)
        max_temp1, max_temp_date1, min_temp1, min_temp_date1, most_humidity2, most_humidity_date1 = calculate.calculate_yearly_month_max(
            weather_record)
        result1.set_weather_results_yearly(
            max_temp1, max_temp_date1, min_temp1, min_temp_date1, most_humidity2, most_humidity_date1)
        report1.year_report(result1)
        print()
    if args.a is not None:
        weather_record = read_file_object.read_files(args.a, args.path)
        avrg_max_tmp1, avrg_min_tmp1, avrg_mean_humidity1 = calculate.calculate_averages(
            weather_record)
        result1.set_weather_results_averages(
            avrg_max_tmp1, avrg_min_tmp1, avrg_mean_humidity1)
        report1.month_average_report(result1)

        print()
    if args.c is not None:
        weather_record = read_file_object.read_files(args.c, args.path)
        date1 = calculate.calculate_max_min(weather_record)
        report1.graphic_report(date1, weather_record)
        print()
