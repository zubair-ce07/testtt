import calendar


class ReportPrinting:
    def __init__(self, results, argument_dict):
        self.results = results
        self.argument_dict = argument_dict

    def printing(self):
        print('\n')
        for argument in self.argument_dict['e']:
            result = self.results.year[argument]
            print(argument, '\n')
            print("Highest: {}C on {} {}".format(result[0][1],
                                                 calendar.month_name[result[0][0].month],
                                                 result[0][0].day))

            print("Lowest: {}C on {} {}".format(result[1][1],
                                                calendar.month_name[result[1][0].month],
                                                result[1][0].day))

            print("Humidity: {}% on {} {}".format(result[2][1],
                                                  calendar.month_name[result[2][0].month],
                                                  result[2][0].day))

        for argument in self.argument_dict['a']:
            year_month = argument.split('_')
            print('\n' + year_month[1], year_month[0], '\n')
            result = self.results.month_average[argument]
            print("Highest Average:", result[0])
            print("Lowest Average:", result[1])
            print("Average Mean Humidity:", result[2])

        for argument in self.argument_dict['c']:
            year_month = argument.split('_')
            print('\n' + year_month[1], year_month[0], '\n')
            mont_record = self.results.month_chart[argument]
            for record in mont_record:
                day = record[0]
                max_temp = int(record[1]) if record[1] is not '' else 0
                min_temp = int(record[2]) if record[2] is not '' else 0
                print( "{}{} {} {}{}".format('\033[91m', day, '+'*max_temp, max_temp, 'C'))
                print("{}{} {} {}{}".format('\033[94m', day, '+'*min_temp, min_temp, 'C'))