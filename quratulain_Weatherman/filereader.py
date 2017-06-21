import fnmatch
import calendar
import csv
import os


class FileReader:
    path = ''
    arg_dict = {}
    month_converter = None

    def __init__(self, args):
        self.path = args.dir_path
        self.generate_arguments_dict(args)

    def generate_arguments_dict(self, args):
        if args.arg_report1:
            year = args.arg_report1
            month_name = '*'
            self.arg_dict['e'] = [year, month_name]

        if args.arg_report2:
            year, month = args.arg_report2.split('/')
            month_name = calendar.month_name[int(month)]
            self.arg_dict['c'] = [year, month_name[:3]]

        if args.arg_report3:
            year, month = args.arg_report3.split('/')
            month_name = calendar.month_name[int(month)]
            self.arg_dict['a'] = [year, month_name[:3]]

    def read_files(self):
        """
        Read the given files and maintain the records in the form of dictionary having file names as keys,
        which further contains file data(list of dictionaries) as values.
        """

        file_data = []
        files_data = {}

        for year, month_name in self.arg_dict.values():
            file_pattern = 'Murree_weather_' + year + '_' + month_name + '.txt'

            for file_name in os.listdir(self.path):
                if fnmatch.fnmatch(file_name, file_pattern) and file_pattern not in files_data:
                    with open(self.path + '/' + file_name, "r") as current_file:
                        reader = csv.DictReader(current_file)

                        for row in reader:
                            record_date = row['PKT'] if row.get('PKST') is None else row['PKST']
                            max_temprature = float('-inf') if row[
                                                                  'Max TemperatureC'] is '' else int(
                                row['Max TemperatureC'])
                            min_temprature = float('inf') if row['Min TemperatureC'] is '' else int(
                                row['Min TemperatureC'])
                            max_humidity = float('-inf') if row['Max Humidity'] is '' else int(
                                row['Max Humidity'])
                            mean_humidity = float('inf') if row[' Mean Humidity'] is '' else int(
                                row[' Mean Humidity'])
                            year, month, day = record_date.split('-')
                            month_name = calendar.month_name[int(month)]

                            file_data.append({

                                'day': int(day), 'year': int(year), 'month': month_name,
                                'maxHumidity': max_humidity, 'meanHumidity': mean_humidity,
                                'minTemprature': min_temprature, 'maxTemprature': max_temprature,

                            })

                        files_data[file_name] = file_data
                        file_data = []

        return files_data
