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
    def report_e(results):
        print('Highest: {}C on {} {} \n'.format(results.max_annual_temp,
              ReportGenerator.month_translation[results.date_max_annual_temp[1]],
              results.date_max_annual_temp[0]))
        print('Lowest: {}C on {} {} \n'.format(results.min_annual_temp,
              ReportGenerator.month_translation[results.date_min_annual_temp[1]],
              results.date_min_annual_temp[0]))
        print('Humidity: {}% on {} {} \n'.format(results.max_annual_hum,
              ReportGenerator.month_translation[results.date_max_annual_hum[1]],
              results.date_min_annual_temp[0]))

    @staticmethod
    def report_a(results):
        print('Highest Average: {}C \n'.format(int(results.max_avg_temp_of_month)))
        print('Lowest Average: {}C \n'.format(int(results.min_avg_temp_of_month)))
        print('Mean Average Humidity: {}% \n'.format(int(results.avg_mean_hum_of_month)))

    @staticmethod
    def report_c(year, month, data):
        counter = 0
        for data_segments in data:
            for data_segment in data_segments:
                if counter == 0:
                    print(ReportGenerator.month_translation[month], year)
                counter += 1
                if data_segment.highest_temp != -100:
                    print("{:02}".format(counter) + "\033[0m", end=' ')
                    print('\033[94m' + '+' * int(data_segment.highest_temp) + '\033[0m', end='')
                    print(" {:02}C".format(data_segment.highest_temp), end='\n')
                    print("{:02}".format(counter), end=' ')
                    print('\033[91m' + '+' * int(data_segment.lowest_temp) + '\033[0m', end='')
                    print(" {:02}C".format(data_segment.lowest_temp), end='\n')

    @staticmethod
    def report_d(year, month, data):
        counter = 1
        for data_segments in data:
            for data_segment in data_segments:
                if counter == 1:
                    print(ReportGenerator.month_translation[month], year)
                if data_segment.highest_temp != -100:
                    print("{:02}".format(counter), end=' ')
                    print('\033[91m' + '+' * data_segment.lowest_temp + '\033[0m', end='')
                    print('\033[94m' + '+' * data_segment.highest_temp + '\033[0m', end='')
                    print(" {:02}C - {:02}C".format
                          (data_segment.lowest_temp,
                           data_segment.highest_temp), end='\n')
                    counter += 1
