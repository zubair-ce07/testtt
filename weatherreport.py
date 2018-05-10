import calendar


class WeatherReport:

    def max_temperature_graph(self, max_temperature):
        print('\033[91m'+'+'*max_temperature,end='')


    def min_temperature_graph(self, min_temperature):
        print('\033[94m'+'+'*min_temperature,end='')


    def get_formatted_date(self, date):
        segmented_date = date.split('-')
        return f'{calendar.month_name[int(segmented_date[1])]} {segmented_date[2]}'


    def monthly_graph(self, monthly_max_temp, monthly_min_temp):
        for index, value in enumerate (monthly_max_temp):
            print('\033[91m' + str(index + 1), end='')
            self.max_temperature_graph(monthly_max_temp[index])
            print ('\033[91m' + '('+str(monthly_max_temp[index]) + ')')
            print('\033[94m' + str(index + 1), end='')
            self.min_temperature_graph(monthly_min_temp[index])
            print ('\033[94m' + '(' + str(monthly_min_temp[index]) + ')')


    def merged_graph(self, monthly_max_temp, monthly_min_temp):
        for index, value in enumerate(monthly_max_temp):
            print(str(index + 1) + ' ', end='')
            self.min_temperature_graph(monthly_min_temp[index])
            self.max_temperature_graph(monthly_max_temp[index])
            print (' %dC - %dC'%(monthly_min_temp[index], monthly_max_temp[index]))


    def display_monthly_weather(self, max_avg_temperature, min_avg_temperature,
                                avg_humidity):
         print(f'Highest Average: {max_avg_temperature}C' +
               f'\nLowest Average: {min_avg_temperature}C' +
               f'\nAverage Mean Humidity: {avg_humidity}%')


    def display_yearly_weather(self, max_temp, max_temp_date, min_temp, min_temp_date,
                               max_humidity, max_humidity_date):
        print(f'Highest Temperature: {max_temp}C on ' +
              f'{self.get_formatted_date(max_temp_date)}' +
              f'\nLowest Temperature: {min_temp}C on ' +
              f'{self.get_formatted_date(min_temp_date)}' +
              f'\nHighest Humidity: {max_humidity}% on ' +
              f'{self.get_formatted_date(max_humidity_date)}')
