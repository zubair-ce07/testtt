class ReportPrinter:

    def _red(self, input_str):
        print(f'\33[31;0m{input_str}\33[0m')

    def _red_raw(self, input_str):
        return f'\33[31;0m{input_str}\33[0m'

    def _blue(self, input_str):
        print(f'\33[34;0m{input_str}\33[0m')

    def _blue_raw(self, input_str):
        return f'\33[34;0m{input_str}\33[0m'

    def high_low_temperature_printer(self, output):

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

    def avg_temperature_printer(self, output):

        output_str = f'Highest Average: {output.avg_max_temp}C\n' \
            f'Lowest Average: {output.avg_min_temp}C\n' \
            f'Average Mean Humidity: {output.avg_mean_humidity}%'
        print(output_str)

    def single_graph_printer(self, weather_records):

        print(f'{weather_records[0].month_name} {weather_records[0].pkt.year}')

        for record in weather_records:
            color_input_max_temp = '+' * abs(record.max_temp) if record.max_temp else ' '
            color_input_min_temp = '+' * abs(record.min_temp) if record.min_temp else ' '

            output_str = f'{record.pkt.day} {self._blue_raw(color_input_min_temp)}' \
                f'{self._red_raw(color_input_max_temp)} {record.min_temp}C - ' \
                f'{record.max_temp}C'
            print(output_str)

    def dual_graph_printer(self, weather_records):

        print(f'{weather_records[0].month_name} {weather_records[0].pkt.year}')

        for record in weather_records:

            color_print_input = '+' * abs(record.max_temp) if record.max_temp else ' '
            output_str = f'{record.pkt.day} {self._red_raw(color_print_input)} ' \
                f'{record.max_temp}C'
            print(output_str)

            color_print_input = '+' * abs(record.min_temp) if record.min_temp else ' '
            output_str = f'{record.pkt.day} {self._blue_raw(color_print_input)} ' \
                f'{record.min_temp}C'
            print(output_str)
