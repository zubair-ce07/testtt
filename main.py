import argparse
from datetime import datetime

import weather


def validate_date(date_text, pattern, error_msg):
    try:
        datetime.strptime(date_text, pattern)
        date_text = date_text.replace('/', '-')
        date_text += '-'
        return date_text
    except ValueError:
        raise argparse.ArgumentTypeError(error_msg)


def valid_year(date_text):
    msg = 'Invalid or out of range year (usage: yyyy) %s' % date_text
    return validate_date(date_text, '%Y', msg)


def valid_year_month(date_text):
    msg = 'Invalid or out of range year (usage: yyyy/mm) %s' % date_text
    return validate_date(date_text, '%Y/%m', msg)


def merge_weather_element_properties(calc_display_format, operation=None):
    return {
        'operation': operation,  # operation perform on element like max/min etc
        'calc_display_format': calc_display_format  # At end calculation will display in this format
    }


def show_weather_attribute_extremes():
    year_weather_readings = wthr_reader.filter_rows_according_pattern(wthr_rows, args.e)
    if year_weather_readings:
        max_temp = merge_weather_element_properties('Highest: {}C on {} {}', 'max')
        min_temp = merge_weather_element_properties('Lowest: {}C on {} {}', 'min')
        max_humd = merge_weather_element_properties('Humidity: {}% on {} {}\n', 'max')
        weather_attributes = [max_temp, min_temp, max_humd]
        attribute_keys = ['Max TemperatureC', 'Min TemperatureC', 'Max Humidity']
        for attribute, key in zip(weather_attributes, attribute_keys):
            attribute_readings = wthr_calc.extract_weather_attribute(year_weather_readings, key)
            attribute_readings = [attr for attr in attribute_readings if attr[key]]
            if 'max' in attribute['operation']:
                attribute.update(max(attribute_readings, key=lambda x: int(x[key])))
            else:
                attribute.update(min(attribute_readings, key=lambda x: int(x[key])))
            wthr_calc.show_calculations(attribute.get('calc_display_format'),
                                        attribute.get(key), attribute.get('day'))
    else:
        print('Sorry, weather files of year {} does not exist\n'.format(args.e))


def show_weather_attribute_avrg():
    month_weather = wthr_reader.filter_rows_according_pattern(wthr_rows, args.a)
    if month_weather:
        avrg_max_temp = merge_weather_element_properties('Highest Average: {}C')
        avrg_min_temp = merge_weather_element_properties('Lowest Average: {}C')
        avrg_mean_humd = merge_weather_element_properties('Average Mean Humidity: {}%\n')
        weather_attributes = [avrg_max_temp, avrg_min_temp, avrg_mean_humd]
        attribute_keys = ['Max TemperatureC', 'Min TemperatureC', ' Mean Humidity']
        for attribute, key in zip(weather_attributes, attribute_keys):
            attribute_readings = wthr_calc.extract_weather_attribute(month_weather, key)
            attribute_readings = [int(attr[key]) for attr in attribute_readings
                                  if attr[key]]
            attribute.update(wthr_calc.calculate_average(attribute_readings))
            wthr_calc.show_calculations(attribute.get('calc_display_format'), attribute.get('avrg'))
    else:
        month = datetime.strptime(args.a, '%Y-%m')
        print('weather file of {} {} doesn\'t exist\n'.format(month.strftime('%B'), month.year))


def show_daily_extreme_temp():
    month_weather = wthr_reader.filter_rows_according_pattern(wthr_rows, args.c)
    if month_weather:
        wthr_calc.show_daily_extreme_temp(month_weather)
    else:
        month = datetime.strptime(args.c, '%Y-%m')
        print('weather file of {} {} doesn\'t exist\n'.format(month.strftime('%B'), month.year))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', help='Enter the directory path which contains weather files')
    parser.add_argument(
        '-c', type=valid_year_month,
        help='(usage: -c yyyy/mm) To see daily maximum and minimum temperature of month')
    parser.add_argument(
        '-a', type=valid_year_month,
        help='(usage: -a yyyy/mm) To see Average of maximum, minimum temperature and '
             'mean Humidity of month')
    parser.add_argument(
        '-e', type=valid_year,
        help='(usage: -e yyyy) To see maximum, minimum temperature and maximum humidity of year')
    args = parser.parse_args()
    wthr_reader = weather.WeatherReader()
    wthr_rows = wthr_reader.read_weather_rows(args.path)
    wthr_calc = weather.WeatherCalculator()
    if args.e:
        show_weather_attribute_extremes()
    if args.a:
        show_weather_attribute_avrg()
    if args.c:
        show_daily_extreme_temp()
