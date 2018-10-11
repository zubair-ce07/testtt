#!/usr/bin/python3.6
from csv_file_data_holder import CsvFileDataHolder
from constants import MONTHS_NAME


class WeatherDataAnalysis:

    def analyse(self, operation, weather_readings, current_year, month_number=0):
        if operation is 'e':
            return self.calculate_yearly_record(weather_readings, current_year)
        elif operation is 'a':
            return self.calculate_monthly_record(
                weather_readings, current_year, month_number)
        else:
            return self.calculate_monthly_record_for_bar_charts(
                weather_readings, current_year, month_number)

    def calculate_yearly_record(self, weather_readings, current_year):
        highest_temp_struct, lowest_temp_struct = [], []
        most_humid_struct, report = [], []
        year_max_temp, year_min_temp, year_highest_humidity = -273, 200, 0
        month_list = weather_readings.get_months_list_by_year(current_year)
        for month in month_list:
            if month is not None:
                max_temp_list = month.get_int_converted_attribute_values(
                    'Max TemperatureC')
                month_max_temp = max(list(filter(None.__ne__, max_temp_list)))
                if year_max_temp <= month_max_temp:
                    highest_temp_struct = [month_max_temp,
                                           MONTHS_NAME[month_list.index(
                                               month)],
                                           max_temp_list.index(month_max_temp)+1]
                    year_max_temp = month_max_temp
                min_temp_list = month.get_int_converted_attribute_values(
                    'Min TemperatureC')
                month_min_temp = min(list(filter(None.__ne__, min_temp_list)))
                if year_min_temp >= month_min_temp:
                    lowest_temp_struct = [month_min_temp,
                                          MONTHS_NAME[month_list.index(month)],
                                          min_temp_list.index(month_min_temp)+1]
                    year_min_temp = month_min_temp
                highest_humidity_list = month.get_int_converted_attribute_values(
                    'Max Humidity')
                month_highest_humid_day = max(list(filter(None.__ne__,
                                                          highest_humidity_list)))
                if year_highest_humidity <= month_highest_humid_day:
                    most_humid_struct = [month_highest_humid_day,
                                         MONTHS_NAME[month_list.index(month)],
                                         highest_humidity_list.index(
                                             month_highest_humid_day)+1]
                    year_highest_humidity = month_highest_humid_day
                report = [highest_temp_struct,
                          lowest_temp_struct, most_humid_struct]
        return report

    def calculate_monthly_record(self, weather_readings, current_year, month_number):
        month_list = weather_readings.get_months_list_by_year(current_year)
        report = []
        month = month_list[month_number]
        if month is not None:
            max_temp_list = month.get_int_converted_attribute_values(
                'Max TemperatureC')
            min_temp_list = month.get_int_converted_attribute_values(
                'Min TemperatureC')
            mean_humidty_list = month.get_int_converted_attribute_values(
                'Mean Humidity')

            report.append(sum(list(filter(None.__ne__, max_temp_list)))
                          / len(list(filter(None.__ne__, max_temp_list))))

            report.append(sum(list(filter(None.__ne__, min_temp_list)))
                          / len(list(filter(None.__ne__, min_temp_list))))

            report.append(sum(list(filter(None.__ne__, mean_humidty_list)))
                          / len(list(filter(None.__ne__, mean_humidty_list))))
        return report

    def calculate_monthly_record_for_bar_charts(self, weather_readings, current_year, month_number):
        month_list = weather_readings.get_months_list_by_year(current_year)
        report = {}
        month = month_list[month_number]
        if month is not None:
            max_temp_list = month.get_int_converted_attribute_values(
                'Max TemperatureC')
            min_temp_list = month.get_int_converted_attribute_values(
                'Min TemperatureC')
            report['high_temprature'] = max_temp_list
            report['low_temprature'] = min_temp_list
        return report
