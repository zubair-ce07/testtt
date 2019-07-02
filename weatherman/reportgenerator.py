class ReportGenerator:

    def __init__(self, weather_records):
        self.weather_records = weather_records

    class _HighLowResult:

        def __init__(self, max_temp_record, max_humidity_record, min_temp_record):
            self.max_temp_record = max_temp_record
            self.max_humidity_record = max_humidity_record
            self.min_temp_record = min_temp_record

    class _AvgTemperatureResult:

        def __init__(self, avg_max_temp, avg_mean_humidity, avg_min_temp):
            self.avg_max_temp = avg_max_temp
            self.avg_mean_humidity = avg_mean_humidity
            self.avg_min_temp = avg_min_temp

    def _red(self, input_str):
        print(f'\33[31;0m{input_str}\33[0m')

    def _red_raw(self, input_str):
        return f'\33[31;0m{input_str}\33[0m'

    def _blue(self, input_str):
        print(f'\33[34;0m{input_str}\33[0m')

    def _blue_raw(self, input_str):
        return f'\33[34;0m{input_str}\33[0m'

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

        max_temp_record = max(max_temp_records, key=lambda x: x.max_temp)
        max_humidity_record = max(max_humidity_records, key=lambda x: x.max_humidity)
        min_temp_record = min(min_temp_records, key=lambda x: x.min_temp)

        return self._HighLowResult(max_temp_record, max_humidity_record, min_temp_record)

    def _avg_temperature_calculator(self, weather_data):

        max_temps = [d.max_temp for d in weather_data if d.max_temp]
        min_temps = [d.min_temp for d in weather_data if d.min_temp]
        mean_humidities = [d.mean_humidity for d in weather_data if d.mean_humidity]

        avg_max_temp = self._mean(max_temps)
        avg_min_temp = self._mean(min_temps)
        avg_mean_humidity = self._mean(mean_humidities)

        return self._AvgTemperatureResult(avg_max_temp, avg_mean_humidity, avg_min_temp)

    def _weather_data_sorter_on_day(self, weather_data):
        return sorted(weather_data, key=lambda x: x.pkt.day)

    def _print_month_year(self, record):
        print(f'{record.month_name} {record.pkt.year}')

    def _high_low_temperature_printer(self, output):

        output_str = f'Highest: {output.max_temp_record.max_temp}C ' \
            f'on {output.max_temp_record.month_name[:3]} ' \
            f'{output.max_temp_record.pkt.day}\n' \
            f'Lowest: {output.min_temp_record.min_temp}C on ' \
            f'{output.min_temp_record.month_name[:3]} ' \
            f'{output.min_temp_record.pkt.day}\n' \
            f'Humidity: {output.max_humidity_record.max_humidity}% on ' \
            f'{output.max_humidity_record.month_name[:3]} ' \
            f'{output.max_humidity_record.pkt.day}'
        print(output_str)

    def _avg_temperature_printer(self, output):

        output_str = f'Highest Average: {output.avg_max_temp}C\n' \
            f'Lowest Average: {output.avg_min_temp}C\n' \
            f'Average Mean Humidity: {output.avg_mean_humidity}%'
        print(output_str)

    def _single_graph_printer(self, sorted_weather_data):

        self._print_month_year(sorted_weather_data[0])

        for record in sorted_weather_data:
            color_input_max_temp = '+' * record.max_temp if record.max_temp else ' '
            color_input_min_temp = '+' * record.min_temp if record.min_temp else ' '

            output_str = f'{record.pkt.day} {self._blue_raw(color_input_min_temp)}' \
                f'{self._red_raw(color_input_max_temp)} {record.min_temp}C - ' \
                f'{record.max_temp}C'
            print(output_str)

    def _dual_graph_printer(self, sorted_weather_data):

        self._print_month_year(sorted_weather_data[0])

        for record in sorted_weather_data:
            color_print_input = '+' * record.max_temp if record.max_temp else 'Data NA'
            output_str = f'{record.pkt.day} {self._red_raw(color_print_input)} ' \
                f'{record.max_temp}C'
            print(output_str)

            color_print_input = '+' * record.min_temp if record.min_temp else 'Data NA'
            output_str = f'{record.pkt.day} {self._blue_raw(color_print_input)} ' \
                f'{record.min_temp}C'
            print(output_str)

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
