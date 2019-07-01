from operator import attrgetter
from collections import namedtuple


HighLowResult = namedtuple('HighLowResult', ['max_temp_record',
                                             'max_humidity_record',
                                             'min_temp_record'])

AvgTemperatureResult = namedtuple('AvgTemperatureResult', ['avg_max_temp',
                                                           'avg_mean_humidity',
                                                           'avg_min_temp'])


class ReportGenerator:

    def __init__(self, weather_records):
        self.weather_records = weather_records

    def _red(self, input_str):
        print('\33[31;0m{}\33[0m'.format(input_str))

    def _red_raw(self, input_str):
        return '\33[31;0m{}\33[0m'.format(input_str)

    def _blue(self, input_str):
        print('\33[34;0m{}\33[0m'.format(input_str))

    def _blue_raw(self, input_str):
        return '\33[34;0m{}\33[0m'.format(input_str)

    def _none_remover_from_map(self, weather_data, attr):
        """removes none from a map and appends all lists into one list of the map"""

        weather_data_clean = []
        for key in weather_data.keys():
            weather_data_clean.extend([d for d in weather_data[key] if getattr(d, attr)])

        return weather_data_clean

    def _mean(self, arr):
        return int(sum(arr) / len(arr))

    def _high_low_temperature_calculator(self, weather_data):

        max_temp_records = self._none_remover_from_map(weather_data, 'max_temp')
        min_temp_records = self._none_remover_from_map(weather_data, 'min_temp')
        max_humidity_records = self._none_remover_from_map(weather_data, 'max_humidity')

        max_temp_record = max(max_temp_records, key=attrgetter('max_temp'))
        max_humidity_record = max(max_humidity_records, key=attrgetter('max_humidity'))
        min_temp_record = min(min_temp_records, key=attrgetter('min_temp'))

        return HighLowResult(max_temp_record, max_humidity_record, min_temp_record)

    def _avg_temperature_calculator(self, weather_data):

        max_temps = [d.max_temp for d in weather_data if d.max_temp]
        min_temps = [d.min_temp for d in weather_data if d.min_temp]
        mean_humidities = [d.mean_humidity for d in weather_data if d.mean_humidity]

        avg_max_temp = self._mean(max_temps)
        avg_min_temp = self._mean(min_temps)
        avg_mean_humidity = self._mean(mean_humidities)

        return AvgTemperatureResult(avg_max_temp, avg_mean_humidity, avg_min_temp)

    def _weather_data_sorter_on_day(self, weather_data):
        return sorted(weather_data, key=lambda x: x.pkt.day)

    def _print_month_year(self, record):
        print('{} {}'.format(record.month_name, record.pkt.year))

    def _high_low_temperature_printer(self, output):

        format_str = 'Highest: {}C on {} {}\nLowest: {}C on {} {}\nHumidity: {}% on {} {}'
        print(format_str.format(output.max_temp_record.max_temp,
                                output.max_temp_record.month_name[:3],
                                output.max_temp_record.pkt.day,
                                output.min_temp_record.min_temp,
                                output.min_temp_record.month_name[:3],
                                output.min_temp_record.pkt.day,
                                output.max_humidity_record.max_humidity,
                                output.max_humidity_record.month_name[:3],
                                output.max_humidity_record.pkt.day,
                                ))

    def _avg_temperature_printer(self, output):

        format_str = 'Highest Average: {}C\nLowest Average: {}C\n' \
                     'Average Mean Humidity: {}%'
        print(format_str.format(output.avg_max_temp, output.avg_min_temp, output.avg_mean_humidity))

    def _single_graph_printer(self, sorted_weather_data):

        self._print_month_year(sorted_weather_data[0])

        for record in sorted_weather_data:

            color_input_max_temp = '+' * record.max_temp if record.max_temp else ' '
            color_input_min_temp = '+' * record.min_temp if record.min_temp else ' '

            print('{} {}{} {}C - {}C'.format(record.pkt.day,
                                             self._blue_raw(color_input_min_temp),
                                             self._red_raw(color_input_max_temp),
                                             record.min_temp, record.max_temp))

    def _dual_graph_printer(self, sorted_weather_data):

        self._print_month_year(sorted_weather_data[0])

        for record in sorted_weather_data:

            color_print_input = '+' * record.max_temp if record.max_temp else 'Data NA'
            print('{} {} {}C'.format(record.pkt.day,
                                     self._red_raw(color_print_input),
                                     record.max_temp))

            color_print_input = '+' * record.min_temp if record.min_temp else 'Data NA'
            print('{} {} {}C'.format(record.pkt.day,
                                     self._blue_raw(color_print_input),
                                     record.min_temp))

    def high_low_temperature(self, year):

        weather_data = self.weather_records[year]
        output = self._high_low_temperature_calculator(weather_data)
        self._high_low_temperature_printer(output)

    def avg_temperature(self, year, month):

        weather_data = self.weather_records[year][month]
        output = self._avg_temperature_calculator(weather_data)
        self._avg_temperature_printer(output)

    def high_low_temperature_single_graph(self, year, month):

        weather_data = self.weather_records[year][month]
        output = self._weather_data_sorter_on_day(weather_data)
        self._single_graph_printer(output)

    def high_low_temperature_dual_graph(self, year, month):

        weather_data = self.weather_records[year][month]
        output = self._weather_data_sorter_on_day(weather_data)
        self._dual_graph_printer(output)
