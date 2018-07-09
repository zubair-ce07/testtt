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
    def annual_report(year, highest_hum, highest_temp, lowest_temp):
        if highest_temp:
            print(f'Highest: {highest_temp.highest_temp}C on '
                  f'{ReportGenerator.month_translation[highest_temp.month]} '
                  f'{highest_temp.day}')
            print(f'Lowest: {lowest_temp.lowest_temp}C on '
                  f'{ReportGenerator.month_translation[lowest_temp.month]} '
                  f'{lowest_temp.day}')
            print(f'Humidity: {highest_hum.highest_hum}% on '
                  f'{ReportGenerator.month_translation[highest_hum.month]} '
                  f'{highest_hum.day} \n')
        else:
            print(f'No weather_readings Found for -e {year}\n')

    @staticmethod
    def month_report(month, year, max_avg_temp, min_avg_temp, mean_avg_hum):
        if max_avg_temp:
            print(f'-a Months Report {ReportGenerator.month_translation[month]} {year}:')
            print(f'Highest Average: {int(max_avg_temp)}C')
            print(f'Lowest Average: {int(min_avg_temp)}C')
            print(f'Mean Average Humidity: {int(mean_avg_hum)}% \n')
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
            print(f'-c {ReportGenerator.month_translation[month]} {year}')
            for day_reading in weather_readings:
                counter = day_reading.day
                print(f'{counter:02}', end=' ')
                print(f'\033[91m' + '+' * day_reading.lowest_temp + '\033[0m', end='')
                print(f'\033[94m' + '+' * day_reading.highest_temp + '\033[0m', end='')
                print(f' {day_reading.lowest_temp:02}C - {day_reading.highest_temp:02}C', end='\n')
        else:
            print(f'No weather_readings Found For -d {ReportGenerator.month_translation[month]} {year}')
        print('\n')
