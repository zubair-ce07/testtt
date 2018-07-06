class ReportGenerator:
    month_translation = {1: 'January',
                         2: 'February',
                         3: 'March',
                         4: 'April',
                         5: 'May',
                         6: 'June',
                         7: 'July',
                         8: 'August',
                         9: 'September',
                         10: 'October',
                         11: 'November',
                         12: 'December'}

    @staticmethod
    def annual_report(year, results):
        if results:
            print(f'-e Annual Report {year}:')
            print(f'Highest: {results.max_annual_temp}C on '
                  f'{ReportGenerator.month_translation[results.date_max_annual_temp[1]]} '
                  f'{results.date_max_annual_temp[0]}')
            print(f'Lowest: {results.min_annual_temp}C on '
                  f'{ReportGenerator.month_translation[results.date_min_annual_temp[1]]} '
                  f'{results.date_min_annual_temp[0]}')
            print(f'Humidity: {results.max_annual_hum}% on '
                  f'{ReportGenerator.month_translation[results.date_max_annual_hum[1]]} '
                  f'{results.date_max_annual_hum[0]} \n')
        else:
            print(f'No weather_readings Found for -e {year}\n')

    @staticmethod
    def month_report(month, year, results):
        if results:
            print(f'-a Months Report {ReportGenerator.month_translation[month]} {year}:')
            print(f'Highest Average: {int(results.max_avg_temp_of_month)}C')
            print(f'Lowest Average: {int(results.min_avg_temp_of_month)}C')
            print(f'Mean Average Humidity: {int(results.avg_mean_hum_of_month)}% \n')
        else:
            print(f'No weather_readings Found for -a {ReportGenerator.month_translation[month]} {year}\n')

    @staticmethod
    def dual_bar_chart_report(year, month, weather_readings):
        if weather_readings:
            print(f' -d {ReportGenerator.month_translation[month]} {year}')
            for day_reading in weather_readings:
                counter = day_reading.day
                print(f'{counter:02}', end=' ')
                print(f'\033[94m' + '+' * int(day_reading.highest_temp) + '\033[0m', end='')
                print(f' {day_reading.highest_temp:02}C', end='\n')
                print(f'{counter:02}', end=' ')
                print(f'\033[91m' + '+' * int(day_reading.lowest_temp) + '\033[0m', end='')
                print(f' {day_reading.lowest_temp:02}C', end='\n')
            print('\n')
        else:
            print(f'No weather_readings Found For -c {ReportGenerator.month_translation[month]} {year}\n')

    @staticmethod
    def single_bar_chart_report(year, month, weather_readings):
        if weather_readings:
            print(f'-d {ReportGenerator.month_translation[month]} {year}')
            for day_reading in weather_readings:
                counter = day_reading.day
                print(f'{counter:02}', end=' ')
                print(f'\033[91m' + '+' * day_reading.lowest_temp + '\033[0m', end='')
                print(f'\033[94m' + '+' * day_reading.highest_temp + '\033[0m', end='')
                print(f' {day_reading.lowest_temp:02}C - {day_reading.highest_temp:02}C', end='\n')
        else:
            print(f'No weather_readings Found For -d {ReportGenerator.month_translation[month]} {year}')
        print('\n')

    @staticmethod
    def display_argument_error_msg(argument):
        print(f'Invalid arguments {argument} Enter in the form of year/month where year is any integer and month is '
              'in range (1-12)\n')
