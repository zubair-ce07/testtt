"""
This module read user input , read files , perform calculation and generate reports
"""
import argparse
import calendar
import csv
import os

from datetime import datetime
from operator import attrgetter


class WeatherReading:
    """The class holds weather data for single day"""
    highest_temp = 0
    lowest_temp = 0
    most_humidity = 0
    mean_humidity = 0
    date = ''

    def __init__(self, date, highest_tmp, lowest_tmp, most_humidity, mean_humidity):
        """The init method stores data for single day"""
        self.highest_temp = int(highest_tmp) if highest_tmp != '' else -273
        self.lowest_temp = int(lowest_tmp) if lowest_tmp != '' else 0
        self.most_humidity = int(most_humidity) if most_humidity != '' else 0
        self.mean_humidity = mean_humidity
        self.date = date


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
            min_temp_date, most_humidity_val,
            most_humidity_date):
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
        print("Maximum: {max_temp_value} C on {date_max_temp} ".format(
            max_temp_value=results.maximum_temp_value,
            date_max_temp=datetime.strftime(date_format, self.MONTH_DAY_FORMAT)))

        date_format = datetime.strptime(
            results.min_temp_date, self.DATE_FORMAT)
        print("Lowest: {min_temp_value} C on {date_min_temp} ".format(
            min_temp_value=results.minimum_temp_value,
            date_min_temp=datetime.strftime(date_format, self.MONTH_DAY_FORMAT)))
        date_format = datetime.strptime(
            results.most_humidity_date, self.DATE_FORMAT)
        print("Humidity: {humidity_value} % on {date_most_humidity} ".format(
            humidity_value=results.most_humidity_value,
            date_most_humidity=datetime.strftime(date_format, self.MONTH_DAY_FORMAT)))

    def month_average_report(self, results):
        """The method prints averages of (max min temperature,mean humidity)"""
        print("Highest Average: {avrg_max_temp} C".
              format(avrg_max_temp=results.average_maximum_temp))
        print("Lowest Average: {avrg_low_temp} C".
              format(avrg_low_temp=results.average_minimum_temp))
        print("Average Mean Humidity: {avrg_mean_humidity} %".
              format(avrg_mean_humidity=results.average_mean_humidity))

    def graphic_report(self, year_and_month, day_data_obj):
        """The method prints the graphic report of month max min temperature"""
        date_format = datetime.strptime(year_and_month, self.DATE_FORMAT)
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
                print("{day} {start_Redcolor} {total_chararters} {end_color} {max_temp_value} C"
                      .format(day=day_num + 1, start_Redcolor='\033[1;31m',
                              total_chararters=total_characters_max_temp,
                              end_color='\033[1;m', max_temp_value=highest_temp_value))
                total_characters_min_temp = '+' * lowest_temp_value
                print("{day} {start_bluecolor} {total_chararters} {end_color} {low_temp_value} C"
                      .format(day=day_num + 1, start_bluecolor='\033[1;34m',
                              total_chararters=total_characters_min_temp,
                              end_color='\033[1;m', low_temp_value=lowest_temp_value))
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
                print("{day} {start_bluecolor} {mintemp} {end_color} {start_redcolor} {maxtemp}\
                        {end_redcolor} {lowtempvalue} C - {hightempvalue} C".format
                      (day=day_num + 1, start_bluecolor='\033[1;34m',
                       mintemp=total_characters_min_temp,
                       end_color='\033[1;m', start_redcolor='\033[1;31m',
                       maxtemp=total_characters_max_temp,
                       end_redcolor='\033[1;m', lowtempvalue=lowest_temp_value,
                       hightempvalue=highest_temp_value))


class DataCalculation:
    """The class performs calculations on weather readings"""

    @staticmethod
    def calculate_yearly_month_max(day_data_obj):
        """The method find maximum,minimum temperature and most humidity"""
        max_temp_day = max(
            [day for day in day_data_obj if day.highest_temp != ''],
            key=attrgetter('highest_temp')
        )
        min_temp_day = min(
            [day for day in day_data_obj if day.lowest_temp != ''],
            key=attrgetter('lowest_temp')
        )
        most_humid_day = max(
            [day for day in day_data_obj if day.most_humidity != ''],
            key=attrgetter('most_humidity')
        )
        year_calculation = {
            'highest_temp': max_temp_day.highest_temp,
            'max_tmp_date': max_temp_day.date,
            'lowest_temp': min_temp_day.lowest_temp,
            'min_tmp_date': min_temp_day.date,
            'most_humidity': most_humid_day.most_humidity,
            'humidity_date': most_humid_day.date}
        return year_calculation

    @staticmethod
    def calculate_averages(day_data_obj):
        """The method calculate averages of maximum,minimum temperature and mean humidity"""
        sum_max_temp = 0
        avrg_max_tmp = 0
        sum_min_temp = 0
        avrg_min_tmp = 0
        sum_mean_humidity = 0
        avrg_mean_humidity = 0
        data_found_count = 0

        max_temp_list = [
            day.highest_temp for day in day_data_obj if day.highest_temp != '']
        sum_max_temp = sum(list(map(int, max_temp_list)))
        data_found_count = len(max_temp_list)
        min_temp_list = [
            day.lowest_temp for day in day_data_obj if day.lowest_temp != '']
        sum_min_temp = sum(list(map(int, min_temp_list)))
        mean_humidity_list = [
            day.mean_humidity for day in day_data_obj if day.mean_humidity != '']
        sum_mean_humidity = sum(list(map(int, mean_humidity_list)))
        avrg_max_tmp = sum_max_temp / data_found_count
        avrg_min_tmp = sum_min_temp / data_found_count
        avrg_mean_humidity = sum_mean_humidity / data_found_count
        month_average_calculation = {
            'avrg_max_tmp':avrg_max_tmp,
            'avrg_min_tmp':avrg_min_tmp,
            'avrg_mean_humidity':avrg_mean_humidity
        }
        return month_average_calculation


class FileParser:
    """The class filters the files and populate data to weather reading class"""

    @staticmethod
    def read_files(year_and_month, path_to_dir):
        """The method read the files"""
        is_month = year_and_month.find('/') > 0
        year = year_and_month.split('/')[0]
        months = []
        all_readings = []

        if is_month:
            months.append(int(year_and_month.split('/')[1]))
        else:
            months = [x for x in range(1, 13)]

        for month in months:
            file_name = "Murree_weather_{year}_{month_abbr}.txt".format(
                year=year,
                month_abbr=calendar.month_abbr[month]
            )
            file_path = path_to_dir + file_name
            if os.path.isfile(file_path):
                with open(file_path, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for reading in reader:
                        date = reading.get('PKT') if reading.get(
                            'PKT') else reading.get('PKST')
                        highest_temp = reading['Max TemperatureC']
                        lowest_temp = reading['Min TemperatureC']
                        most_humidity = reading['Max Humidity']
                        mean_humidity = reading[' Mean Humidity']
                        all_readings.append(
                            WeatherReading(date, highest_temp, lowest_temp,
                                           most_humidity, mean_humidity))

        return all_readings


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", help="enter the year", type=str)
    parser.add_argument("-a", help="enter the year", type=str)
    parser.add_argument("-c", help="enter the year", type=str)
    parser.add_argument("path", help="enter the year", type=str)
    args = parser.parse_args()
    result1 = WeatherResults()
    report1 = Report()
    if args.e is not None:
        weather_record = FileParser.read_files(args.e, args.path)
        calculated_results = DataCalculation.calculate_yearly_month_max(weather_record)
        result1.set_weather_results_yearly(
            max_tmp=calculated_results['highest_temp'],
            max_temp_date=calculated_results['max_tmp_date'],
            min_temp_date=calculated_results['min_tmp_date'],
            min_tmp=calculated_results['lowest_temp'],
            most_humidity_val=calculated_results['most_humidity'],
            most_humidity_date=calculated_results['humidity_date']
        )
        report1.year_report(result1)
        print()
    if args.a is not None:
        weather_record = FileParser.read_files(args.a, args.path)
        calculated_results = DataCalculation.calculate_averages(
            weather_record)
        result1.set_weather_results_averages(
            avrg_max=calculated_results['avrg_max_tmp'],
            avrg_min=calculated_results['avrg_min_tmp'],
            avrg_mean_humid=calculated_results['avrg_mean_humidity']
        )
        report1.month_average_report(result1)

        print()
    if args.c is not None:
        weather_record = FileParser.read_files(args.c, args.path)
        report1.graphic_report(weather_record[0].date, weather_record)
        print()
