import argparse

import WeatherCalc
import WeatherDataReader
import Results
import ReportGenerator


def process_annual_report(data):
    highest_temp = WeatherCalc.WeatherAnalyzer().highest_temp_of_year(data)
    lowest_temp = WeatherCalc.WeatherAnalyzer().lowest_temp_of_year(data)
    highest_hum = WeatherCalc.WeatherAnalyzer().highest_hum_of_year(data)

    day_max_annual_hum = data[highest_hum].day
    month_max_annual_hum = data[highest_hum].month
    year_max_annual_hum = data[highest_hum].year
    date_max_annual_hum = [day_max_annual_hum, month_max_annual_hum, year_max_annual_hum]

    day_max_annual_temp = data[highest_temp].day
    month_max_annual_temp = data[highest_temp].month
    year_max_annual_temp = data[highest_temp].year
    date_max_annual_temp = [day_max_annual_temp, month_max_annual_temp, year_max_annual_temp]

    day_min_annual_temp = data[lowest_temp].day
    month_min_annual_temp = data[lowest_temp].month
    year_min_annual_temp = data[lowest_temp].year
    date_min_annual_temp = [day_min_annual_temp, month_min_annual_temp, year_min_annual_temp]

    max_annual_hum = data[highest_hum].highest_hum
    min_annual_temp = data[lowest_temp].lowest_temp
    max_annual_temp = data[highest_temp].highest_temp
    result_dict = {"date_max_annual_temp": date_max_annual_temp,
                   "date_max_annual_hum": date_max_annual_hum,
                   "date_min_annual_temp": date_min_annual_temp,
                   "max_annual_hum": max_annual_hum,
                   "max_annual_temp": max_annual_temp,
                   "min_annual_temp": min_annual_temp}
    result = Results.Results(result_dict)
    ReportGenerator.ReportGenerator().annual_report(result)


def process_month_report(data):
    max_avg_temp = WeatherCalc.WeatherAnalyzer().highest_avg_temp_of_month(data)
    min_avg_temp = WeatherCalc.WeatherAnalyzer().lowest_avg_temp_of_month(data)
    mean_avg_hum = WeatherCalc.WeatherAnalyzer().average_mean_humidity_of_month(data)
    result_dict = {"mean_avg_hum": mean_avg_hum,
                   "min_avg_temp": min_avg_temp,
                   "max_avg_temp": max_avg_temp}
    result = Results.Results(result_dict)
    ReportGenerator.ReportGenerator().month_report(result)


def process_dual_bar_report(argument, data):
    year = int(argument[0])
    month = int(argument[1])
    ReportGenerator.ReportGenerator().dual_bar_chart_report(year, month, data)


def process_single_bar_report(argument, data):
    year = int(argument[0])
    month = int(argument[1])
    ReportGenerator.ReportGenerator().single_bar_chart_report(year, month, data)


def is_valid(argument):
    try:
        arguments = argument.split('/')
        year = int(arguments[0])
        month = int(arguments[1])
        if year in range(2004, 2017) and month in range(1, 13):
            return True
        else:
            return False
    except:
        return False


def month_resolution(month_number):
    month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                  7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    return month_dict[month_number]


def run(my_path, args):
    if args.type_e:
        weather_data = WeatherDataReader.WeatherDataReader().read_yearly_data(my_path, args.type_e)
        process_annual_report(weather_data)
    if args.type_a:
        if is_valid(args.type_a):
            arguments = args.type_a.split('/')
            month_str = month_resolution(int(arguments[1]))
            year = int(arguments[0])
            weather_data = WeatherDataReader.WeatherDataReader().read_monthly_data(
                my_path, year, month_str)
            process_month_report(weather_data)
        else:
            print("Invalid arguments. Kindly provide them in the form of -a year/month "
                  "where year is in range [2004-2016] and month is in range [1-12]")
    if args.type_c:
        if is_valid(args.type_c):
            arguments = args.type_c.split('/')
            month_str = month_resolution(int(arguments[1]))
            year = int(arguments[0])
            weather_data = WeatherDataReader.WeatherDataReader().read_monthly_data(
                my_path, year, month_str)
            process_dual_bar_report(arguments, weather_data)
        else:
            print("Invalid arguments. Kindly provide them in the form of -c year/month "
                  "where year is in range [2004-2016] and month is in range [1-12]")
    if args.type_d:
        if is_valid(args.type_d):
            arguments = args.type_d.split('/')
            month_str = month_resolution(int(arguments[1]))
            weather_data = WeatherDataReader.WeatherDataReader().read_monthly_data(
                my_path, int(arguments[0]), month_str)
            process_single_bar_report(arguments, weather_data)
        else:
            print("Invalid arguments. Kindly provide them in the form of -d year/month "
                  "where year is in range [2004-2016] and month is in range [1-12]")


def main():
    my_path = 'weatherfiles'
    parser = argparse.ArgumentParser(description="Report will be generated according to the Arguments")
    parser.add_argument("-e", "--type_e", type=int, help="Annual Report", choices=range(2004, 2017))
    parser.add_argument("-a", "--type_a", type=str, help="Monthly Report")
    parser.add_argument("-c", "--type_c", type=str, help="Dual Bar Chart")
    parser.add_argument("-d", "--type_d", type=str, help="Single Bar Chart")
    args = parser.parse_args()
    run(my_path, args)


if __name__ == '__main__':
    main()
