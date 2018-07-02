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
        print('Highest: {}C on {} {} \n'.format(results.maxAnnualTemp,
              ReportGenerator.month_translation[results.dateMaxAnnualTemp[1]],
              results.dateMaxAnnualTemp[0]))
        print('Lowest: {}C on {} {} \n'.format(results.minAnnualTemp,
              ReportGenerator.month_translation[results.dateMinAnnualTemp[1]],
              results.dateMinAnnualTemp[0]))
        print('Humidity: {}% on {} {} \n'.format(results.maxAnnualHum,
              ReportGenerator.month_translation[results.dateMaxAnnualHum[1]],
              results.dateMinAnnualTemp[0]))

    @staticmethod
    def report_a(results):
        print('Highest Average: {}C \n'.format(int(results.maxAvgTempOfMonth)))
        print('Lowest Average: {}C \n'.format(int(results.minAvgTempOfMonth)))
        print('Mean Average Humidity: {}% \n'.format(int(results.avgMeanHumOfMonth)))


    @staticmethod
    def report_c(year, month, data):
        counter = 0
        for dataSegmen in data:
            for dataSegment in dataSegmen:
                try:
                    if dataSegment.year == year and dataSegment.month == month:
                        if counter == 0:
                            print(ReportGenerator.month_translation[month], year)
                        counter += 1
                        if dataSegment.highestT != -100:
                            print("{:02}".format(counter) + "\033[0m", end=' ')
                            for a in range(int(dataSegment.highestT)):
                                print('\033[94m' + '+' + '\033[0m', end='')
                            print(" {:02}".format(dataSegment.highestT), end='')
                            print('\n')
                            print("{:02}".format(counter), end=' ')
                            for a in range(int(dataSegment.lowestT)):
                                print('\033[91m' + '+' + '\033[0m', end='')
                            print(" {:02}".format(dataSegment.lowestT), end='')
                            print('\n')
                except:
                    continue

    @staticmethod
    def report_d(year, month, data):
        counter = 1
        for dataSegmen in data:
            for dataSegment in dataSegmen:
                try:
                    if dataSegment.year == year and dataSegment.month == month:
                        if counter == 1:
                            print(ReportGenerator.month_translation[month], year)

                        if dataSegment.highestT != -100:
                            print("{:02}".format(counter), end=' ')
                            print('\033[91m' + '+' * dataSegment.lowestT + '\033[0m', end='')
                            print('\033[94m' + '+' * dataSegment.highestT + '\033[0m', end='')
                            print(" {:02}C - {:02}C".format
                                  (dataSegment.lowestT,
                                   dataSegment.highestT), end='')
                            print('\n')
                        counter += 1
                except:
                    continue