class ReportPrinter:

    _red_t = '\33[31;0m{}\33[0m'
    _blue_t = '\33[34;0m{}\33[0m'
    _purple_t = '\33[95;0m{}\33[0m'

    def high_low_temperature_printer(self, report):
        print(f'Highest: {report.max_temp_record.max_temp}C '
              f'on {report.max_temp_record.pkt.strftime("%b")} '
              f'{report.max_temp_record.pkt.day}',
              f'Lowest: {report.min_temp_record.min_temp}C on '
              f'{report.min_temp_record.pkt.strftime("%b")} '
              f'{report.min_temp_record.pkt.day}',
              f'Humidity: {report.max_humidity_record.max_humidity}% on '
              f'{report.max_humidity_record.pkt.strftime("%b")} '
              f'{report.max_humidity_record.pkt.day}', sep='\n')

    def avg_temperature_printer(self, report):
        print(f'Highest Average: {report.avg_max_temp}C',
              f'Lowest Average: {report.avg_min_temp}C',
              f'Average Mean Humidity: {report.avg_mean_humidity}%', sep='\n')

    def single_graph_printer(self, weather_records):
        print(f'{weather_records[0].pkt.strftime("%B")} {weather_records[0].pkt.year}')

        for record in weather_records:
            red_plus_sign = '+' * abs(record.max_temp) if record.max_temp else ' '
            blue_plus_sign = '+' * abs(record.min_temp) if record.min_temp else ' '
            purple_min_max_temp = self._purple_t.format(f'{record.min_temp}C - {record.max_temp}C')
            print(f'{self._purple_t.format(record.pkt.day)}', f'{self._blue_t.format(blue_plus_sign)}'
                  f'{self._red_t.format(red_plus_sign)}', f'{self._purple_t.format(purple_min_max_temp)}',
                  sep=' ')

    def dual_graph_printer(self, weather_records):
        print(f'{weather_records[0].pkt.strftime("%B")} {weather_records[0].pkt.year}')

        for record in weather_records:
            color_plus_sign = '+' * abs(record.max_temp) if record.max_temp else ''
            purple_temp = f'{record.max_temp}C'
            print(f'{self._purple_t.format(record.pkt.day)}', f'{self._red_t.format(color_plus_sign)}',
                  f'{self._purple_t.format(purple_temp)}', sep=' ')

            color_plus_sign = '+' * abs(record.min_temp) if record.min_temp else ''
            purple_temp = f'{record.min_temp}C'

            print(f'{self._purple_t.format(record.pkt.day)}', f'{self._blue_t.format(color_plus_sign)}',
                  f'{self._purple_t.format(purple_temp)}', sep=' ')
