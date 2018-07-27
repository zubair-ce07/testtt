import calendar


class WeatherStatisticsReport:
    def __init__(self, results):
        self.results = results
        self.description_dictionary = {
                'avg_max_temp': 'Highest Temperature Average: {}C',
                'avg_min_temp': 'Lowest Temperature Average: {}C',
                'avg_mean_humidity': 'Mean Humidity Average: {}%'
            }

    def print_extrema_statistics(self, argument):
        """This function is used to print maximum temperature, minimum temperature and maximum humidity
        Extrema means both maximum and minimum"""
        results = self.results.year[argument]
        if results:
            print('Statistics of', argument, '\n')
            if results['max_temp']:
                print('Highest temperature: {}C on {} {}'.format(results['max_temp'].max_temperature,
                                                                 calendar.month_name[results['max_temp'].date.month],
                                                                 results['max_temp'].date.day))
            if results['min_temp']:
                print('Lowest temperature: {}C on {} {}'.format(results['min_temp'].min_temperature,
                                                                calendar.month_name[results['min_temp'].date.month],
                                                                results['min_temp'].date.day))
            if results['max_humidity']:
                print('Highest Humidity: {}% on {} {}'.format(results['max_humidity'].max_humidity,
                                                              calendar.month_name[results['max_humidity'].date.month],
                                                              results['max_humidity'].date.day))

    def print_average_statistics(self, argument):
        month_statistics = self.results.month_average[argument]
        if month_statistics:
            year_month = argument.split('_')
            print('\nStatistics of ' + year_month[1], year_month[0], '\n')
            for key, value in month_statistics.items():
                print(self.description_dictionary[key].format(value))

    def get_line_style(self, value):
        return '-' if value < 0 else '+'

    def get_chart_line(self, record):
        day = record.date.day
        minimum_temp_bar, maximum_temp_bar = '', ''
        maximum_temp, minimum_temp, separator = '', '', ''

        if record.max_temperature is not None:
            maximum_temp_bar = '\033[91m' + '+'*record.max_temperature
            maximum_temp = str(record.max_temperature) + 'C'
            separator = '-'

        if record.min_temperature is not None:
            style = self.get_line_style(record.min_temperature)
            minimum_temp_bar = '\033[94m' + style*abs(record.min_temperature)
            minimum_temp = str(record.min_temperature) + 'C ' + separator

        return '{} {}{} {} {}'.format(day, minimum_temp_bar, maximum_temp_bar, minimum_temp, maximum_temp)

    def plot_chart(self, argument):
        month_record = self.results.month_chart[argument]
        if month_record:
            year_month = argument.split('_')
            print('\nBar chart of ' + year_month[1], year_month[0])
            print('\n- is used instead of + for negative temperatures!\n')
            for record in month_record:
                print(self.get_chart_line(record))
