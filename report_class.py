import calendar

class ReportPrinting:
    def __init__(self, results, args):
        self.results = results
        self.args = args

    def get_file_name_key_plus_month_name(self, year_month):
        month_abbrv = calendar.month_abbr[int(year_month[1])]
        month_name = calendar.month_name[int(year_month[1])]
        file_name_key = "lahore_weather_{}_{}".format(year_month[0], month_abbrv)
        return file_name_key, month_name

    def printing(self):
        print('\n')
        for arg_e in self.args.e:
            print(arg_e, '\n')
            result = self.results.year[str(arg_e)]
            print("Highest:", result[0])
            print("Lowest:", result[1])
            print("Humidity:", result[2])

        for arg_a in self.args.a:
            year_month = arg_a.split('/')
            file_name_key, month_name = self.get_file_name_key_plus_month_name(year_month)
            print('\n' + month_name, year_month[0], '\n')
            result = self.results.month_average[file_name_key]
            print("Highest Average:", result[0])
            print("Lowest Average:", result[1])
            print("Average Mean Humidity:", result[2])

        for arg_c in self.args.c:
            year_month = arg_a.split('/')
            file_name_key, month_name = self.get_file_name_key_plus_month_name(year_month)
            print('\n' + month_name, year_month[0], '\n')
            for result in self.results.month_chart[file_name_key]:
                print(result)

            for result in self.results.bonus[file_name_key]:
                print(result)




