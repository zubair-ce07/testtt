import calendar


class WeatherReport:

    def max_temperature_graph(self, max_temperature):
        print('\033[91m'+'+'*max_temperature, end='')

    def min_temperature_graph(self, min_temperature):
        print('\033[94m'+'+'*min_temperature, end='')

    def get_formatted_date(self, date):
        segmented_date = date.split('-')
        return f'{calendar.month_name[int(segmented_date[1])]} {segmented_date[2]}'

    def monthly_graph(self, weather_records):
        max_tempertaures = [temperature.max_temp for temperature in weather_records]
        min_tempertaures = [temperature.min_temp for temperature in weather_records]
        for index, value in enumerate(max_tempertaures):
            print('\033[91m' + str(index + 1), end='')
            self.max_temperature_graph(max_tempertaures[index])
            print ('\033[91m' + '('+str(max_tempertaures[index]) + ')')
            print('\033[94m' + str(index + 1), end='')
            self.min_temperature_graph(min_tempertaures[index])
            print ('\033[94m' + '(' + str(min_tempertaures[index]) + ')')

    def merged_graph(self, weather_records):
        max_tempertaures = [temperature.max_temp for temperature in weather_records]
        min_tempertaures = [temperature.min_temp for temperature in weather_records]
        for index, value in enumerate(max_tempertaures):
            print(str(index + 1) + ' ', end='')
            self.min_temperature_graph(max_tempertaures[index])
            self.max_temperature_graph(min_tempertaures[index])
            print (' %dC - %dC' % (max_tempertaures[index], min_tempertaures[index]))

    def display_monthly_weather(self, max_avg_temperature, min_avg_temperature,
                                max_avg_humidity):
         print(f'Highest Average: {max_avg_temperature}C' +
               f'\nLowest Average: {min_avg_temperature}C' +
               f'\nAverage Mean Humidity: {max_avg_humidity}%')

    def display_yearly_weather(self, max_temperature, min_temperature, max_humidity):
        print(f'Highest Temperature: {max_temperature.max_temp}C on ' +
              f'{self.get_formatted_date(max_temperature.date)}' +
              f'\nLowest Temperature: {min_temperature.min_temp}C on ' +
              f'{self.get_formatted_date(min_temperature.date)}' +
              f'\nHighest Humidity: {max_humidity.max_humidity}% on ' +
              f'{self.get_formatted_date(max_humidity.date)}')
