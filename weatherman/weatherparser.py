import os
import calendar

from weatherrecord import WeatherRecord


class WeatherParser:

    def __init__(self, path):
        self.path = path

    def yearly_weather_parser(self, year):
        weather_records = []
        file_names = os.listdir(path=self.path)

        for file_name in file_names:

            current_file_year = int(file_name.split('_')[2])

            if current_file_year == year:
                current_file_path = os.path.join(self.path, file_name)

                with open(current_file_path, mode='r') as file_data:
                    file_contents = file_data.read()
                    records = file_contents.split('\n')
                    records = records[1:-1]

                    for record in records:
                        record = record.split(',')

                        weather_records.append(WeatherRecord(
                            pkt=record[0],
                            max_temp=int(record[1]) if record[1] else None,
                            min_temp=int(record[3]) if record[3] else None,
                            max_humidity=int(record[7]) if record[7] else None
                        ))

        return weather_records

    def monthly_weather_parser(self, month, year):
        weather_records = []
        file_names = os.listdir(path=self.path)

        for file_name in file_names:
            months_map = dict((v,k) for k,v in enumerate(calendar.month_abbr))
            current_file_month = months_map[file_name.split('_')[3][:3]]
            current_file_year = int(file_name.split('_')[2])

            if current_file_month == month and current_file_year == year:
                current_file_path = os.path.join(self.path, file_name)

                with open(current_file_path, mode='r') as file_data:
                    file_contents = file_data.read()
                    records = file_contents.split('\n')
                    records = records[1:-1]

                    for record in records:
                        record = record.split(',')
                        weather_records.append(WeatherRecord(
                            pkt=record[0],
                            max_temp=int(record[1]) if record[1] else None,
                            min_temp=int(record[3]) if record[3] else None,
                            mean_humidity=int(record[8]) if record[8] else None
                        ))

        return weather_records