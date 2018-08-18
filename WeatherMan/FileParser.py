from glob import glob
import os
import csv
from datetime import datetime


class FileParser:
    """This Class Read all files and make a nested dictionary of every day"""

    def __init__(self, directory):
        self.directory = directory
        self.weather_record = {}

    def file_reader(self):
        """This function will read data from file and make a list"""

        report_paths = glob(
            os.path.join(
                self.directory,
                'lahore_weather_[0-9]*_[A-Z][a-z]*.txt'
            ))

        if report_paths:
            for report_path in report_paths:
                with open(report_path, 'r') as report_file:
                    next(report_file)
                    reader = csv.DictReader(report_file)
                    for row in reader:
                        if 'PKST' in row.keys():
                            if '<!' not in row['PKST']:
                                date = datetime.strptime(
                                    row['PKST'],
                                    "%Y-%m-%d"
                                    )
                            else:
                                continue
                        else:
                            if '<!' not in row['PKT']:
                                date = datetime.strptime(
                                    row['PKT'],
                                    "%Y-%m-%d"
                                    )
                            else:
                                continue
                        choose_data = {
                            'Max TemperatureC': row['Max TemperatureC'],
                            'Min TemperatureC': row['Min TemperatureC'],
                            'Max Humidity': row['Max Humidity'],
                            'Min Humidity': row[' Min Humidity']
                        }
                        self.weather_record[date] = choose_data
        else:
            print("This Directory doesn't contain any weather report")
            exit(0)
        return self.weather_record
