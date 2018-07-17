import calendar


class ReportPrinting:
    def __init__(self, results):
        self.results = results

    def is_numeric(self, number):
        try:
            int(number)
            return True
        except ValueError:
            return False

    def print_results_for_year(self, argument):
        print('\n')
        result = self.results.year[argument]
        print(argument, '\n')
        print('Highest: {}C on {} {}'.format(result['max_temp'].max_temperature,
                                             calendar.month_name[result['max_temp'].date.month],
                                             result['max_temp'].date.day))

        print('Lowest: {}C on {} {}'.format(result['min_temp'].min_temperature,
                                            calendar.month_name[result['min_temp'].date.month],
                                            result['min_temp'].date.day))

        print('Humidity: {}% on {} {}'.format(result['max_humidity'].max_humidity,
                                              calendar.month_name[result['max_humidity'].date.month],
                                              result['max_humidity'].date.day))

    def print_results_for_month(self, argument):
        year_month = argument.split('_')
        print('\n' + year_month[1], year_month[0], '\n')
        result = self.results.month_average[argument]
        print('Highest Average:', result['avg_max_temp'])
        print('Lowest Average:', result['avg_min_temp'])
        print('Average Mean Humidity:', result['avg_mean_humidity'])

    def plot_chart_for_month(self, argument):
        year_month = argument.split('_')
        print('\n' + year_month[1], year_month[0], '\n')
        mont_record = self.results.month_chart[argument]
        print('\n- is used instead of + for negative temperatures!\n')
        for record in mont_record:
            day = record.date.day
            if self.is_numeric(record.max_temperature):
                max_temp = int(record.max_temperature)
                print('{}{} {} {}{}'.format('\033[91m', day, '+' * max_temp, max_temp, 'C'))
            else:
                print('{}{} {}{}'.format('\033[91m', day, 'None ', 'C'))

            if self.is_numeric(record.min_temperature):
                min_temp = int(record.min_temperature)
                style = '+'
                if min_temp < 0:
                    style = '-'
                print('{}{} {} {}{}'.format('\033[94m', day, style*abs(min_temp), min_temp, 'C'))
            else:
                print('{}{} {}{}'.format('\033[94m', day, 'None ', 'C'))
