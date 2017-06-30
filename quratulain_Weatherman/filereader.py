import fnmatch
import calendar
import csv
import os


class FileReader:
    def __init__(self, args):
        self.args = args

    def read_files(self):
        path = self.args.dir_path
        report_records = {'report1': [], 'report2': [], 'report3': []}
        report1_pattern, report2_pattern, report3_pattern = '', '', ''

        if self.args.arg_report1:
            year = self.args.arg_report1
            report1_pattern = 'Murree_weather_' + year + '_*.txt'

        if self.args.arg_report2:
            year, month = self.args.arg_report2.split('/')
            month_name = calendar.month_name[int(month)]
            report2_pattern = 'Murree_weather_' + year + '_' + month_name[:3] + '.txt'

        if self.args.arg_report3:
            year, month = self.args.arg_report3.split('/')
            month_name = calendar.month_name[int(month)]
            report3_pattern = 'Murree_weather_' + year + '_' + month_name[:3] + '.txt'

        for file_name in os.listdir(path):
            pattern1_matched = False
            if fnmatch.fnmatch(file_name, report1_pattern):
                pattern1_matched = True

            pattern2_matched = False
            if fnmatch.fnmatch(file_name, report2_pattern):
                pattern2_matched = True

            pattern3_matched = False
            if fnmatch.fnmatch(file_name, report3_pattern):
                pattern3_matched = True

            with open(path + '/' + file_name, "r") as current_file:
                reader = csv.DictReader(current_file)
                for row in reader:
                    record = self.generate_record(row)

                    if pattern1_matched:
                        report_records['report1'].append(record)

                    if pattern2_matched:
                        report_records['report2'].append(record)

                    if pattern3_matched:
                        report_records['report3'].append(record)

        return report_records

    def generate_record(self, row):
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
