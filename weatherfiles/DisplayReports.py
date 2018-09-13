"""
This class display reports on console
"""
import calendar


class DisplayReports:
    @staticmethod
    def print_yearly_high_low_humidity_report(result):
        """
        Print yearly report for the results  provided
        :param result: a dictionary of results after computations
        """
        print(result['highest']['PKT'].year)

        max_tempC = int(result['highest']['Max TemperatureC'])
        day_max_tempc = result['highest']['PKT'].day
        month_max_tempc = calendar.month_name[result['highest']['PKT'].month]

        min_tempC = int(result['lowest']['Min TemperatureC'])
        day_min_tempc = result['lowest']['PKT'].day
        month_min_tempc = calendar.month_name[result['lowest']['PKT'].month]

        humidity = int(result['humidity']['Max Humidity'])
        day_max_humid = result['humidity']['PKT'].day
        month_max_humid = calendar.month_name[result['humidity']['PKT'].month]

        print('Highest: {}C on {} {}'.format(max_tempC, month_max_tempc, day_max_tempc))
        print('Lowest: {}C on {} {}'.format(min_tempC, month_min_tempc, day_min_tempc))
        print('Humidity: {}% on {} {}\n'.format(humidity, month_max_humid, day_max_humid))

    @staticmethod
    def print_monthly_report(result, date):
        """
        this method prints the monthly report in highest , lowest and mean humidity average from result
        :param result: is a dictionary containing results after computations
        :param date: is yyyy/mm format date for which results are given
        :return:
        """
        print(date)

        print('Highest Average: {0:.2f}C'.format(result['Highest Average']))
        print('Lowest Average: {0:.2f}C'.format(result['Lowest Average']))
        print('Average Mean Humidity: {0:.2f}%\n'.format(result['Average Mean Humidity']))

    @staticmethod
    def print_monthly_charts(result, date):
        """
        This method prints the bar chart for each key in result dictionary
        :param result: is dictionary containing high and low temperature of each day of month
        :param date: the yyyy/mm format date for which results are given
        :return:
        """
        year, month = date.split('/')

        print(calendar.month_name[int(month)] + ' ' + year)

        color_red = '\033[1;31m'
        color_blue = '\033[1;34m'
        color_normal = '\033[m'

        for day, temps in sorted(result.items()):
            output_high_temp = '{} {}{}{} {}C'.format(
                day,
                color_red,
                ('*' * temps[0]),
                color_normal,
                temps[0]
            )
            output_low_temp = '{} {}{}{} {}C'.format(
                day,
                color_blue,
                ('*' * temps[1]),
                color_normal,
                temps[1]
            )

            output = '{}\n{}'.format(output_high_temp, output_low_temp)
            print(output)

        print('BONUS:')
        for day, temps in sorted(result.items()):
            output = '{} {}{}{}{}{} {}C-{}C'.format(
                day,
                color_blue,
                '*' * temps[1],
                color_red,
                '*' * temps[0],
                color_normal,
                temps[1],
                temps[0],
            )

            print(output)
