import csv
import datetime
import glob

from weatherrecord import WeatherRecord


class WeatherParser:

    def __init__(self, path):

        self.path = path
        self.weather_records = self._parse_weather_records()

    def _parse_weather_records(self):

        file_paths = glob.glob(f'{self.path}Murree_weather_*.txt')
        weather_records = {}

        for file_path in file_paths:

            with open(file_path, mode='r') as csv_file:

                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0

                for row in csv_reader:

                    if line_count:
                        date_and_time = datetime.datetime.strptime(row[0], '%Y-%m-%d').date()

                        if date_and_time.year not in weather_records.keys():
                            weather_records[date_and_time.year] = {}

                        if date_and_time.month not in weather_records[date_and_time.year].keys():
                            weather_records[date_and_time.year][date_and_time.month] = []

                        weather_records[date_and_time.year][date_and_time.month].append(
                            WeatherRecord(
                                pkt=date_and_time,
                                max_temp=int(row[1]) if row[1] else None,
                                min_temp=int(row[3]) if row[3] else None,
                                max_humidity=int(row[7]) if row[7] else None,
                                mean_humidity=int(row[8]) if row[8] else None,
                                # %B fullname %b shortname
                                month_name=date_and_time.strftime('%B')
                            )
                        )

                    line_count += 1

        return weather_records
