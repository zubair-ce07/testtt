"""
This class display reports on console
"""
import calendar


class DisplayReports:
    @staticmethod
    def print_year_report(result):
        """
        Print yearly report for the results  provided
        :param result: a dictionary of results after computations
        """

        year, month, day_high = result['date highest tempc'].split('-')
        month_high = calendar.month_name[int(month)]

        year, month, day_low = result['date lowest tempc'].split('-')
        month_low = calendar.month_name[int(month)]

        year, month, day_humid = result['date humidity'].split('-')
        month_humid = calendar.month_name[int(month)]

        print(
            'Highest: {}C on {} {}\n'.format(result['highest tempc'], month_high, day_high) +
            'Lowest: {}C on {} {}\n'.format(result['lowest tempc'], month_low, day_low) +
            'Humidity: {}% on {} {}\n'.format(result['humidity'], month_humid, day_humid)
        )

    @staticmethod
    def print_monthly_report(result):
        """
        this method prints the monthly report in highest , lowest and mean humidity average from result
        :param result: is a dictionary containing results after computations
        :param date: is yyyy/mm format date for which results are given
        :return:
        """
        print(
            'Highest Average: {}C \n'.format(result['Highest Average']) +
            'Lowest Average: {}C \n'.format(result['Lowest Average']) +
            'Average Mean Humidity: {}% \n'.format(result['Average Mean Humidity'])
        )

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

        red = '\033[1;31m'
        blue = '\033[1;34m'
        normal = '\033[m'

        for day, temps in sorted(result.items()):
            output_high_temp = '{} {}{}{} {}C'.format(
                day,
                red,
                ('*' * temps[0]),
                normal,
                temps[0]
            )
            output_low_temp = '{} {}{}{} {}C'.format(
                day,
                blue,
                ('*' * temps[1]),
                normal,
                temps[1]
            )

            output = '{}\n{}'.format(output_high_temp, output_low_temp)
            print(output)

        print('BONUS:')
        for day, temps in sorted(result.items()):
            output = '{} {}{}{}{}{} {}C-{}C'.format(
                day,
                blue,
                '*'*temps[1],
                red,
                '*'*temps[0],
                normal,
                temps[1],
                temps[0],
            )

            print(output)

