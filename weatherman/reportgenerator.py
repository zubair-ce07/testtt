from operator import attrgetter
from collections import namedtuple


HighLowResult = namedtuple('HighLowResult', ['max_temp_record',
                                             'max_humidity_record',
                                             'min_temp_record'])

AvgTemperatureResult = namedtuple('AvgTemperatureResult', ['avg_max_temp',
                                                           'avg_mean_humidity',
                                                           'avg_min_temp'])


class ReportGenerator:

    def _red(self, input_str):
        print('\33[31;0m' + input_str + '\33[0m')

    def _red_raw(self, input_str):
        return '\33[31;0m' + input_str + '\33[0m'

    def _blue(self, input_str):
        print('\33[34;0m' + input_str + '\33[0m')

    def _blue_raw(self, input_str):
        return '\33[34;0m' + input_str + '\33[0m'

    def high_low_temperature(self, weather_data):

        max_temp_records = [data for data in weather_data if data.max_temp is not None]
        min_temp_records = [data for data in weather_data if data.min_temp is not None]
        max_humidity_records = [data for data in weather_data if data.max_humidity is not None]

        max_temp_record = max(max_temp_records, key=attrgetter('max_temp'))
        max_humidity_record = max(max_humidity_records, key=attrgetter('max_humidity'))
        min_temp_record = min(min_temp_records, key=attrgetter('min_temp'))

        final_report = HighLowResult(max_temp_record, max_humidity_record, min_temp_record)

        format_str = 'Highest: {}C on {} {}\nLowest: {}C on {} {}\nHumidity: {}% on {} {}'
        print(format_str.format(max_temp_record.max_temp,
                                max_temp_record.month_name,
                                max_temp_record.day,
                                min_temp_record.min_temp,
                                min_temp_record.month_name,
                                min_temp_record.day,
                                max_humidity_record.max_humidity,
                                max_humidity_record.month_name,
                                max_humidity_record.day,
                                ))
        return final_report

    def avg_temperature(self, weather_data):

        max_temps = [data.max_temp for data in weather_data if data.max_temp is not None]
        min_temps = [data.min_temp for data in weather_data if data.min_temp is not None]
        mean_humidities = [data.mean_humidity for data in weather_data if data.mean_humidity is not None]

        avg_max_temp = self._mean(max_temps)
        avg_min_temp = self._mean(min_temps)
        avg_mean_humidity = self._mean(mean_humidities)

        final_result = AvgTemperatureResult(avg_max_temp, avg_mean_humidity, avg_min_temp)

        format_str = 'Highest Average: {}C\nLowest Average: {}C\n' \
                     'Average Mean Humidity: {}%'

        print(format_str.format(avg_max_temp, avg_min_temp, avg_mean_humidity))
        return final_result

    def _mean(self, arr):
        return int(sum(arr) / len(arr))

    def high_low_temperature_single_graph(self, weather_data):

        print('{} {}'.format(weather_data[0].month_name, weather_data[0].year))
        sorted_weather_records = sorted(weather_data, key=lambda x: x.day)

        for record in sorted_weather_records:
            color_input_max_temp = '+' * record.max_temp if record.max_temp is not None else ' '
            color_input_min_temp = '+' * record.min_temp if record.min_temp is not None else ' '

            print('{} {}{} {}C - {}C'.format(record.day,
                                             self._blue_raw(color_input_min_temp),
                                             self._red_raw(color_input_max_temp),
                                             record.min_temp, record.max_temp))

    def high_low_temperature_dual_graph(self, weather_data):

        print('{} {}'.format(weather_data[0].month_name, weather_data[0].year))
        sorted_weather_records = sorted(weather_data, key=lambda x: x.day)

        for record in sorted_weather_records:
            color_print_input = '+' * record.max_temp if record.max_temp is not None else 'Data NA'
            print('{} {} {}C'.format(record.day,
                                     self._red_raw(color_print_input),
                                     record.max_temp))

            color_print_input = '+' * record.min_temp if record.min_temp is not None else 'Data NA'
            print('{} {} {}C'.format(record.day,
                                     self._blue_raw(color_print_input),
                                     record.min_temp))
