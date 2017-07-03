import fnmatch
import calendar
import csv
import os


class FileReader:
    def __init__(self, args):
        self.args = args

    def read_files(self):
        path = self.args.dir_path
        files_matched = {}
        report_records = {}
        patterns = self.generate_patterns()

        for file_name in os.listdir(path):
            for report_name, file_pattern in patterns.items():
                if fnmatch.fnmatch(file_name, file_pattern):
                    files_matched.setdefault(file_name, []).append(report_name)

        for file_name, report_names in files_matched.items():
            file_path = os.path.join(path, file_name)
            with open(file_path, "r") as current_file:
                reader = csv.DictReader(current_file)
                for row in reader:
                    record = self.generate_record(row)
                    for report_name in report_names:
                        report_records.setdefault(report_name, []).append(record)

        return report_records

    def generate_patterns(self):
        pattern = {}

        if self.args.yearly_report:
            year = self.args.yearly_report
            pattern['yearly_report'] = 'Murree_weather_' + year + '_*.txt'

        if self.args.monthly_report:
            year, month = self.args.monthly_report.split('/')
            month_name = calendar.month_abbr[int(month)]
            pattern['monthly_report'] = 'Murree_weather_' + year + '_' + month_name + '.txt'

        if self.args.temp_graph:
            year, month = self.args.temp_graph.split('/')
            month_name = calendar.month_abbr[int(month)]
            pattern['temp_graph'] = 'Murree_weather_' + year + '_' + month_name + '.txt'

        return pattern

    @staticmethod
    def generate_record(row):
        record_date = row['PKT'] if row.get('PKST') is None else row['PKST']

        max_temp = row['Max TemperatureC']
        max_temp = float('-inf') if max_temp is '' else int(max_temp)

        min_temp = row['Min TemperatureC']
        min_temp = float('inf') if min_temp is '' else int(min_temp)

        max_humidity = row['Max Humidity']
        max_humidity = float('-inf') if max_humidity is '' else int(max_humidity)

        mean_humidity = row[' Mean Humidity']
        mean_humidity = float('inf') if mean_humidity is '' else int(mean_humidity)

        year, month, day = record_date.split('-')
        month_name = calendar.month_name[int(month)]

        record = {'day': int(day), 'year': int(year), 'month': month_name,
                  'maxHumidity': max_humidity, 'meanHumidity': mean_humidity,
                  'minTemprature': min_temp, 'maxTemprature': max_temp, }

        return record
