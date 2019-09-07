import calendar
import sys
from ReportGenerator import ReportGenerator
from Parser import Parser
from Validator import Validator


def main():
    if not Validator.argument_validation(sys.argv):
        exit()
    else:
        index = 2  # skipping First 2 arg as they are file name and path
        while index < len(sys.argv):
            # get flag_indexes[] of the total indexes encounter for -a flag in the command line argument
            flag_indexes = [i for i, f in enumerate(sys.argv) if f == '-a']
            flag_iter = 0  # Variable to iterate over flag_indexes
            while flag_iter < len(flag_indexes):
                year, month = Parser.date_tokenizer(sys.argv[flag_indexes[flag_iter] + 1])
                if not Validator.year_validator(year, sys.argv[1] + '/weatherfiles/') \
                        or not Validator.month_validation(month):
                    exit()
                path = f'{sys.argv[1]}/weatherfiles/Murree_weather_{year}_{calendar.month_abbr[month]}.txt'
                index += 2
                flag_iter += 1
                print(ReportGenerator.calculate_monthly_report(Parser.read_file(path)))
                print()
            # get flag_indexes[] of the total indexes encounter for -e flag in the command line argument
            flag_indexes = [i for i, f in enumerate(sys.argv) if f == '-e']
            flag_iter = 0
            while flag_iter < len(flag_indexes):
                year = sys.argv[flag_indexes[flag_iter] + 1]
                if not Validator.year_validator(year, sys.argv[1] + '/weatherfiles/'):
                    exit()
                reading_list = list()
                month = 1
                while month <= 12:
                    path = f'{sys.argv[1]}/weatherfiles/Murree_weather_{year}_{calendar.month_abbr[month]}.txt'
                    reading_list = reading_list + Parser.read_file(path)
                    month += 1
                print(ReportGenerator.calculate_yearly_report(reading_list))
                index += 2
                flag_iter += 1
            # get flag_indexes[] of the total indexes encounter for -c flag in the command line argument
            flag_indexes = [i for i, f in enumerate(sys.argv) if f == '-c']
            flag_iter = 0
            while flag_iter < len(flag_indexes):
                year, month = Parser.date_tokenizer(sys.argv[flag_indexes[flag_iter] + 1])
                if not Validator.month_validation(month) \
                        or not Validator.year_validator(year, f'{sys.argv[1]}/weatherfiles/'):
                    exit()
                path = f'{sys.argv[1]}/weatherfiles/Murree_weather_{year}_{calendar.month_abbr[month]}.txt'
                index += 2
                flag_iter += 1
                print(ReportGenerator.calculate_chart_report(Parser.read_file(path)))
                print()


main()
