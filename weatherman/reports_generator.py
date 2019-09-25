from datetime import datetime


class ReportsGenerator:

    @staticmethod
    def bonus_chart(data):

        """Prints minimum and maximum temperature of each day for a given month
        minimum temperature in blue and maximum in red color.
        """
        max_temp_values = data['max_temperature']
        min_temp_values = data['min_temperature']
        date_values = data['max_temp_date']

        for (max_temp, min_temp, max_day) in zip(max_temp_values, min_temp_values, date_values):
            max_day = max_day.split('-')[2]
            print(max_day + ' ', end='')
            print("\033[1;34m+\033[1;m" * min_temp, end='')
            print("\033[1;31m+\033[1;m" * max_temp, end='')
            print(f' {min_temp}C-{max_temp}C')

    @staticmethod
    def display_extrems(extremes):

        """ Displays values of maximum temperature, minimum temperature and most humid day """

        max_temp_day = datetime.strptime(extremes['max_temp_date'], '%Y-%m-%d')
        max_temp_day_formatted = max_temp_day.strftime('%B %d')
        min_temp_day = datetime.strptime(extremes['min_temp_date'], '%Y-%m-%d')
        min_temp_day_formatted = min_temp_day.strftime('%B %d')
        max_humid_day = datetime.strptime(extremes['max_humidity_date'],
                                          '%Y-%m-%d')
        max_humid_day_formatted = max_humid_day.strftime('%B %d')

        print(
            f'Highest: {extremes["max_temperature"]}C on {max_temp_day_formatted}')
        print(
            f'Lowest: {extremes["min_temperature"]}C on {min_temp_day_formatted}')
        print(
            f'Humidity: {extremes["max_humidity"]}% on {max_humid_day_formatted}')

    @staticmethod
    def display_averages(avg_values):
        print(f'Highest Average: {avg_values["avg_max_temperature"]}C')
        print(f'Lowest Average: {avg_values["avg_min_temperature"]}C')
        print(f'Average Mean Humidity: {avg_values["avg_mean_humidity"]}%')
