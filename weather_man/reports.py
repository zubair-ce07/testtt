from weather_man.reporttype import ReportType
from weather_man import weathercalculations, helpers
from weather_man.weathermanconstants import WeatherManConstants


def generate_report(report_type, weather_readings):
    if report_type == ReportType.YEARLY.value:
        highest_temp_reading = weathercalculations.get_highest_temperature_reading(weather_readings)
        lowest_temp_reading = weathercalculations.get_lowest_temperature_reading(weather_readings)
        most_humid_day_reading = weathercalculations.get_most_humid_day(weather_readings)

        print(f'{WeatherManConstants.HIGHEST_LABEL} {highest_temp_reading.max_temperature_c}'
              f'{WeatherManConstants.TEMPERATURE_CENTIGRADE_LABEL}'
              f' {WeatherManConstants.ON_MESSAGE} '
              f'{helpers.convert_str_to_date(highest_temp_reading.reading_date, WeatherManConstants.DATE_MONTH_FULL_NAME_FORMAT)}'
              f' {helpers.convert_str_to_date(highest_temp_reading.reading_date, WeatherManConstants.DATE_DAY_FORMAT)}'
              )
        print(f'{WeatherManConstants.LOWEST_LABEL} {lowest_temp_reading.max_temperature_c}'
              f'{WeatherManConstants.TEMPERATURE_CENTIGRADE_LABEL}'
              f' {WeatherManConstants.ON_MESSAGE} '
              f'{helpers.convert_str_to_date(lowest_temp_reading.reading_date, WeatherManConstants.DATE_MONTH_FULL_NAME_FORMAT)} '
              f'{helpers.convert_str_to_date(lowest_temp_reading.reading_date, WeatherManConstants.DATE_DAY_FORMAT)}'
              )
        print(f'{WeatherManConstants.HUMIDITY_LABEL} {most_humid_day_reading.max_temperature_c}'
              f'{WeatherManConstants.PERCENT_LABEL}'
              f' {WeatherManConstants.ON_MESSAGE} '
              f'{helpers.convert_str_to_date(most_humid_day_reading.reading_date, WeatherManConstants.DATE_MONTH_FULL_NAME_FORMAT)}'
              f' {helpers.convert_str_to_date(most_humid_day_reading.reading_date, WeatherManConstants.DATE_DAY_FORMAT)}'
              )
        print(WeatherManConstants.CHART_TEMP_SEPARATOR * WeatherManConstants.DIVIDER_LENGTH)

    if report_type == ReportType.MONTHLY.value:
        average_highest_temperature = weathercalculations.get_highest_temperature_average_value(weather_readings)
        average_lowest_temperature = weathercalculations.get_lowest_temperature_average_value(weather_readings)
        average_mean_humidity = weathercalculations.get_mean_humid_day_average(weather_readings)

        print(f'{WeatherManConstants.HIGHEST_AVERAGE_LABEL} {average_highest_temperature}{WeatherManConstants.TEMPERATURE_CENTIGRADE_LABEL}'
              )
        print(f'{WeatherManConstants.LOWEST_AVERAGE_LABEL} {average_lowest_temperature}{WeatherManConstants.TEMPERATURE_CENTIGRADE_LABEL}'
              )
        print(f'{WeatherManConstants.AVERAGE_MEAN_HUMIDITY_LABEL} {average_mean_humidity}{WeatherManConstants.PERCENT_LABEL}'
              )
        print(WeatherManConstants.CHART_TEMP_SEPARATOR * WeatherManConstants.DIVIDER_LENGTH)

    if report_type == ReportType.MONTHLY_WITH_CHART.value:
        draw_chart_for_lowest_and_highest_temperature_each_day_bonus(weather_readings)
        print(WeatherManConstants.CHART_TEMP_SEPARATOR * WeatherManConstants.DIVIDER_LENGTH)


def draw_chart_for_lowest_and_highest_temperature_each_day(weather_readings):
    loop_index = 0
    for reading in weather_readings:
        if loop_index == 0:
            print(helpers.convert_str_to_date(reading.reading_date,
                                              WeatherManConstants.DATE_MONTH_FULL_NAME_FORMAT),
                  helpers.convert_str_to_date(reading.reading_date,
                                              WeatherManConstants.DATE_YEAR_FORMAT),
                  )
        loop_index = loop_index + 1
        if reading.min_temperature_c != WeatherManConstants.INVALID_DATA:
            chart_bar_string = WeatherManConstants.CHART_TEMP_BAR_ICON * reading.min_temperature_c
            print(f'{WeatherManConstants.CHART_TEMP_BAR_LABEL_COLOR} '
                  f'{helpers.convert_str_to_date(reading.reading_date, WeatherManConstants.DATE_DAY_FORMAT)}'
                  f'{WeatherManConstants.CHART_TEMP_BAR_COLD_COLOR}{chart_bar_string}'
                  f'{WeatherManConstants.CHART_TEMP_BAR_LABEL_COLOR}{reading.min_temperature_c}'
                  f'{WeatherManConstants.TEMPERATURE_CENTIGRADE_LABEL}'
                  )
        if reading.max_temperature_c != WeatherManConstants.INVALID_DATA:
            chart_bar_string = WeatherManConstants.CHART_TEMP_BAR_ICON * reading.max_temperature_c
            print(f'{WeatherManConstants.CHART_TEMP_BAR_LABEL_COLOR} '
                  f'{helpers.convert_str_to_date(reading.reading_date, WeatherManConstants.DATE_DAY_FORMAT)}'
                  f'{WeatherManConstants.CHART_TEMP_BAR_HOT_COLOR}{chart_bar_string}'
                  f'{WeatherManConstants.CHART_TEMP_BAR_LABEL_COLOR}{reading.max_temperature_c}'
                  f'{WeatherManConstants.TEMPERATURE_CENTIGRADE_LABEL}'
                  )


def draw_chart_for_lowest_and_highest_temperature_each_day_bonus(weather_readings):
    loop_index = 0
    for reading in weather_readings:
        if loop_index == 0:
            print(helpers.convert_str_to_date(reading.reading_date,
                                              WeatherManConstants.DATE_MONTH_FULL_NAME_FORMAT),
                  helpers.convert_str_to_date(reading.reading_date,
                                              WeatherManConstants.DATE_YEAR_FORMAT),
                  )
        loop_index = loop_index + 1
        if reading.min_temperature_c != WeatherManConstants.INVALID_DATA:
            hot_chart_bar_string = WeatherManConstants.CHART_TEMP_BAR_HOT_COLOR + \
                                   WeatherManConstants.CHART_TEMP_BAR_ICON * reading.max_temperature_c
            cold_chart_bar_string = WeatherManConstants.CHART_TEMP_BAR_COLD_COLOR + \
                                    WeatherManConstants.CHART_TEMP_BAR_ICON * reading.min_temperature_c

            print(f'{WeatherManConstants.CHART_TEMP_BAR_LABEL_COLOR}'
                  f' {helpers.convert_str_to_date(reading.reading_date, WeatherManConstants.DATE_DAY_FORMAT)}'
                  f'{cold_chart_bar_string}{hot_chart_bar_string}'
                  f'{WeatherManConstants.CHART_TEMP_BAR_LABEL_COLOR}{reading.min_temperature_c}'
                  f'{WeatherManConstants.TEMPERATURE_CENTIGRADE_LABEL}'
                  f' {WeatherManConstants.CHART_TEMP_SEPARATOR}'
                  f'{WeatherManConstants.CHART_TEMP_BAR_LABEL_COLOR}{reading.max_temperature_c}'
                  f'{WeatherManConstants.TEMPERATURE_CENTIGRADE_LABEL}'
                  )
