import calendar


class ReportPrinting:
    def __init__(self, results):
        self.results = results

    def print_results_for_year(self, argument):
        result = self.results.year[argument]
        if result:
            print('Statistics of', argument, '\n')
            max_temp_record = result['max_temp']
            if max_temp_record:
                print('Highest temperature: {}C on {} {}'.format(max_temp_record.max_temperature,
                                                                 calendar.month_name[max_temp_record.date.month],
                                                                 max_temp_record.date.day))
            min_temp_record = result['min_temp']
            if min_temp_record:
                print('Lowest temperature: {}C on {} {}'.format(min_temp_record.min_temperature,
                                                                calendar.month_name[min_temp_record.date.month],
                                                                min_temp_record.date.day))
            max_humidity_record = result['max_humidity']
            if max_humidity_record:
                print('Highest Humidity: {}% on {} {}'.format(max_humidity_record.max_humidity,
                                                              calendar.month_name[max_humidity_record.date.month],
                                                              max_humidity_record.date.day))

    def print_results_for_month(self, argument):
        result = self.results.month_average[argument]
        if result:
            year_month = argument.split('_')
            print('\nStatistics of ' + year_month[1], year_month[0], '\n')
            if result['avg_max_temp']:
                print('Highest Temperature Average:', result['avg_max_temp'])
            if result['avg_min_temp']:
                print('Lowest Temperature Average :', result['avg_min_temp'])
            if result['avg_mean_humidity']:
                print('Mean Humidity Average:', result['avg_mean_humidity'])

    def get_line_style(self, value):
        if value < 0:
            return '-'
        return '+'

    def get_formatted_string(self, record):
        day = record.date.day
        if record.max_temperature:
            if record.min_temperature:
                style = self.get_line_style(record.min_temperature)
                return '{} {}{}{}{} {}C - {}C'.format(day,
                                                      '\033[94m', style*abs(record.min_temperature),
                                                      '\033[91m', '+'*record.max_temperature,
                                                      record.min_temperature, record.max_temperature)
            else:
                return '{}{} {} {}C'.format('\033[91m', day, '+'*record.max_temperature, record.max_temperature)
        else:
            if record.min_temperature:
                style = self.get_line_style(record.min_temperature)
                return '{}{} {} {}C'.format('\033[94m', day, style*abs(record.min_temperature),
                                            record.min_temperature)
        return None

    def plot_chart_for_month(self, argument):
        mont_record = self.results.month_chart[argument]
        if mont_record:
            year_month = argument.split('_')
            print('\nBar chart of ' + year_month[1], year_month[0])
            print('\n- is used instead of + for negative temperatures!\n')
            for record in mont_record:
                formatted_string = self.get_formatted_string(record)
                if formatted_string:
                    print(formatted_string)
