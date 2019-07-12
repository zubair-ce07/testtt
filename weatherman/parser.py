import os
import csv
from collections import defaultdict
from os import listdir
from os.path import isfile, join


class Parser:
    """Parser class to extract data and parse it."""

    years = []
    months = []

    def extract_years_months(self, data_path):

        files = [f for f in listdir(data_path) if isfile(join(data_path, f))]
        for file_ in files:
            if not file_.startswith('.'):
                file_ = file_.split("_")
                if file_[2] not in self.years:
                    self.years.append(file_[2])
                if file_[3].split('.')[0] not in self.months:
                    self.months.append(file_[3].split('.')[0])
        return

    def read_files(self, data_path):
        """This function will read all the weather data."""

        self.extract_years_months(data_path)
        # Dictionary to store all the data
        data_for_all_months = {}

        # Read all files
        for year in self.years:
            for month in self.months:

                file_ = f'{data_path}Murree_weather_{year}_{month}.txt'

                if os.path.exists(file_):

                    monthly_readings = self.file_parser(file_)
                    data_for_all_months[year + "_" + month] = monthly_readings

        return data_for_all_months, self.years, self.months

    def file_parser(self, month_file):
        """This function will read a File in a dictionary object."""

        monthly_readings = defaultdict(lambda: [])
        with open(month_file, newline='\n') as f:
            reader = csv.DictReader(f)
            for reading in reader:
                for header_val, value in reading.items():
                    if value:

                        header_val = header_val.replace(" ", '')
                        if header_val in ['PKST', 'PKT', 'Events']:

                            monthly_readings[header_val].append(value)
                        elif header_val.replace(" ", '') in [
                            'MaxVisibilityKm', 'MeanVisibilityKm',
                            'MinVisibilitykM', 'Precipitationmm',
                            'MeanSeaLevelPressurehPa'
                        ]:

                            monthly_readings[header_val].append(float(value))
                        else:

                            monthly_readings[header_val].append(int(value))
                    else:

                        monthly_readings[header_val].append(None)

        return monthly_readings
