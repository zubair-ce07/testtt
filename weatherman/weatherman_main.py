import argparse
import calendar
from datetime import datetime

import error_messages
from weather_files_reader import WeatherDataReader
from reports_calculator import ReportsCalculator
from reports_generator import ReportsGenerator


def validate_year(year):
    try:
        return datetime.strptime(year, '%Y').strftime('%Y')
    except ValueError:
        print(error_messages.YEAR_VALIDATION_ERROR)

def validate_year_month(date):
    try:
        return datetime.strptime(date, '%Y/%m').strftime('%Y/%m')
    except ValueError:
        print(error_messages.MONTH_VALIDATION_ERROR)

def parse_date(year_month):    
    date = year_month.split('/')
    year, month = date[0], date[1]
    month_name = calendar.month_abbr[int(month)]

    return {'year': year, 'month': month_name}

def main():
    parser = argparse.ArgumentParser(description='Weatherman app')
    parser.add_argument('path')
    parser.add_argument('-e', type=validate_year, nargs='+')
    parser.add_argument('-a', type=validate_year_month, nargs='+')
    parser.add_argument('-c', type=validate_year_month, nargs='+')
    args = parser.parse_args()

    weather_reader = WeatherDataReader()
    args_dict = vars(args)
                   
    if  args_dict['e']  != None:          
        file_names_e = WeatherDataReader.read_yearly_file_names(args_dict['path'], args_dict['e'][0])

        if file_names_e:
            weather_data = weather_reader.read_files(file_names_e)
            min_and_max_values = ReportsCalculator.calculate_min_max(weather_data)
            ReportsGenerator.display_min_max(min_and_max_values)                           
        else:
            print(error_messages.YEAR_FILE_NOT_FOUND_ERROR)                

    if  args_dict['a']  != None:        
        date = parse_date(args_dict['a'][0])
        file_names_a = WeatherDataReader.read_monthly_file_names(args_dict['path'], date['year'], date['month'])

        if file_names_a:
            weather_data = weather_reader.read_files(file_names_a)
            avg_values = ReportsCalculator.calculate_averages(weather_data)
            ReportsGenerator.display_averages(avg_values)                            
        else:
            print(error_messages.MONTH_FILE_NOT_FOUND_ERROR)

    if  args_dict['c']  != None:        
        date = parse_date(args_dict['c'][0])
        file_names_c = WeatherDataReader.read_monthly_file_names(args_dict['path'], date['year'], date['month'])
        
        if file_names_c:
            weather_data = weather_reader.read_files(file_names_c)
            ReportsGenerator.display_month_bar_chart(weather_data)                           
        else:
            print(error_messages.MONTH_FILE_NOT_FOUND_ERROR)


if __name__ == '__main__':
    main()