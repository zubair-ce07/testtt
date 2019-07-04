class ReportPrinter:

    _red_t = '\33[31;0m{}\33[0m'
    _blue_t = '\33[34;0m{}\33[0m'

    def high_low_temperature_printer(self, output):
        print(f'Highest: {output.max_temp_record.max_temp}C '
              f'on {output.max_temp_record.pkt.strftime("%b")} '
              f'{output.max_temp_record.pkt.day}\n'
              f'Lowest: {output.min_temp_record.min_temp}C on '
              f'{output.min_temp_record.pkt.strftime("%b")} '
              f'{output.min_temp_record.pkt.day}\n'
              f'Humidity: {output.max_humidity_record.max_humidity}% on '
              f'{output.max_humidity_record.pkt.strftime("%b")} '
              f'{output.max_humidity_record.pkt.day}')

    def avg_temperature_printer(self, output):
        print(f'Highest Average: {output.avg_max_temp}C\n'
              f'Lowest Average: {output.avg_min_temp}C\n'
              f'Average Mean Humidity: {output.avg_mean_humidity}%')

    def single_graph_printer(self, weather_records):
        print(f'{weather_records[0].pkt.strftime("%B")} {weather_records[0].pkt.year}')

        for record in weather_records:
            color_input_max_temp = '+' * abs(record.max_temp) if record.max_temp else ' '
            color_input_min_temp = '+' * abs(record.min_temp) if record.min_temp else ' '

            print(f'{record.pkt.day} {self._blue_t.format(color_input_min_temp)}'
                  f'{self._red_t.format(color_input_max_temp)} {record.min_temp}C - '
                  f'{record.max_temp}C')

    def dual_graph_printer(self, weather_records):
        print(f'{weather_records[0].pkt.strftime("%B")} {weather_records[0].pkt.year}')

        for record in weather_records:
            color_print_input = '+' * abs(record.max_temp) if record.max_temp else ' '
            print(f'{record.pkt.day} {self._red_t.format(color_print_input)} '
                  f'{record.max_temp}C')

            color_print_input = '+' * abs(record.min_temp) if record.min_temp else ' '
            print(f'{record.pkt.day} {self._blue_t.format(color_print_input)} '
                  f'{record.min_temp}C')
