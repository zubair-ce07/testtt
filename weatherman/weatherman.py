import argparse

from FilesParser import FilesParser
from CalculateResults import CalculateResults
from Reports import Reports


arguments = argparse.ArgumentParser(description='Arguments for weatherman.py')
arguments.add_argument('Path', metavar='path', type=str, help='the path to the files')
arguments.add_argument('-e', help='Display Highest, Lowest temperatures and most humid day of given year')
arguments.add_argument('-a', help='Average highest and lowest temps for given month')
arguments.add_argument('-c', help='Display bars of temps of warmest and coldest days of given month')
arguments.add_argument('-d', help='[BONUS] Display bars of temps of warmest and coldest days of given month')

args = arguments.parse_args()
path = args.Path

year_e = args.e
month_a = args.a
month_c = args.c
month_d = args.d

highest_temp_yearly_days = {}
lowest_temp_yearly_days = {}
highest_humid_yearly_days = {}

highest_mnthly_for_avg = {}
lowest_mnthly_for_avg = {}
mean_humidity_monthly_days = {}


highest_temp_year = {}
lowest_temp_year = {}
most_humid_day_year = {}

f_parser = FilesParser()
result_calculator = CalculateResults()
results = Reports()

if(year_e is not None):
    f_parser.populate_yearly_temps(highest_temp_yearly_days, lowest_temp_yearly_days, highest_humid_yearly_days, path,
                                   year_e)
    result_calculator.yearly_highest_temp(highest_temp_yearly_days, highest_temp_year)
    result_calculator.yearly_lowest_temp(lowest_temp_yearly_days, lowest_temp_year)
    result_calculator.yearly_most_humid_day(highest_humid_yearly_days, most_humid_day_year)

    results.show_yearly_results(highest_temp_year, lowest_temp_year, most_humid_day_year)

if(month_a is not None):
    f_parser.populate_monthly_avgs(highest_mnthly_for_avg, lowest_mnthly_for_avg, mean_humidity_monthly_days, path,
                                   month_a)
    avg_highest_monthly=result_calculator.avg(highest_mnthly_for_avg)
    avg_lowest_monthly=result_calculator.avg(lowest_mnthly_for_avg)
    avg_mean_humidity=result_calculator.avg(mean_humidity_monthly_days)

    results.show_monthly_avgs(avg_highest_monthly, avg_lowest_monthly, avg_mean_humidity)

if(month_c is not None):
    results.show_monthly_temps(path, month_c, False)

if(month_d is not None):
    results.show_monthly_temps(path, month_d, True)