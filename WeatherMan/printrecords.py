import calendar

from colors import Colors


class PrintRecords:
    @staticmethod
    def print_yearly_record(max_temperature, min_temperature, max_humidity, year):
        print('\n' + year)
        print('Highest: {}C on {}'.format(max_temperature.max_temp, max_temperature.date.strftime('%B %d')))
        print('Lowest: {}C on {}'.format(min_temperature.min_temp, min_temperature.date.strftime('%B %d')))
        print('Humidity: {}% on {}'.format(max_humidity.max_humid, max_humidity.date.strftime('%B %d')))

    @staticmethod
    def avg_monthly_record(avg_max_temperature, avg_min_temperature, avg_mean_humidity, year, month):
        print('\n' + calendar.month_name[int(month)] + ' ' + year)
        print('Highest Average: {}C'.format(avg_max_temperature))
        print('Lowest Average: {}C'.format(avg_min_temperature))
        print('Average Mean Humidity: {}%'.format(avg_mean_humidity))

    @staticmethod
    def comparative_daily_record(data, year, month):
        print('\n' + calendar.month_name[int(month)] + ' ' + year)
        for row in data:
            print(Colors.BOLD + str(row.date.day) + ' ' + Colors.BLUE + '+' * abs(row.min_temp) + Colors.RED
                  + '+' * abs(row.max_temp) + Colors.BOLD + ' ' + str(row.min_temp)
                  + 'C - ' + str(row.max_temp) + 'C')
