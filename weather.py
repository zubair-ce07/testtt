from os import listdir
from os.path import isfile, join, isdir
from pprint import pprint
import glob

import pandas as pd


MIN_TEMPC_COL = "Min TemperatureC"
MAX_TEMPC_COL = "Max TemperatureC"
MAX_HUMIDITY_COL = "Max Humidity"
MEAN_HUMIDITY_COL = "Mean Humidity"
DATE_COL = "PKST"


class Weather:
    def __init__(self):
        self.weather_files_dict = {}
        self.dataframe = None

    def get_month_and_year(self, filename):
        """
            Returns a tuple(year, month)
            filename: format is(TEXT_weather_yyyy_mmm.txt)
        """
        return (filename.split('_')[-2], filename.split('_')[-1].split('.')[0])

    def update_weather_files_dict(self, key, file_path):
        if key not in self.weather_files_dict:
            self.weather_files_dict[key] = [file_path]
        else:
            self.weather_files_dict[key].append(file_path)

    def process_files(self, dir_path, year=None):
        """
            process the given directory for weather files and store the files
            path in a dictionary for later processing

            weather_files_dict = {year: list of file paths of given year} 
            if @year is None

            weather_files_dict = {month: list of file paths of given year}
            if @year is provided (yyyy)
        """
        # TEXT_weather_yyyy_mmm.txt
        for file_path in glob.glob(
            dir_path + '*[0-9]*[a-zA-Z]*.txt'
        ):
            file_year, file_month = self.get_month_and_year(file_path)
            if year:  # update weather_files_dict for months of given year
                self.update_weather_files_dict(file_month, file_path)
            else:  # update weather_files_dict for year
                self.update_weather_files_dict(file_year, file_path)

    def get_dataframe_from_files(self, file_paths):
        """
            receives a list of file paths and return a single dataframe
        """
        dfs = []
        for file_path in file_paths:
            df = pd.read_csv(file_path, index_col=None, engine="python")
            # Renaming PKT to PKST to sync the columns over multiple files
            if "PKT" in df.columns:
                df.rename(columns={"PKT": "PKST"}, inplace=True)

            dfs.append(df)

        dataframe = pd.concat(dfs, axis=0, sort=False, ignore_index=True)

        return dataframe

    def preprocess_dataframe(self):
        # Removing NANs from PKST column (date column)
        self.dataframe.dropna(subset=[DATE_COL], inplace=True)
        # Removing extra spaces from the column on either side
        columns = [c.strip() for c in self.dataframe.columns]
        self.dataframe.columns = columns

    def get_year_stats(self, year):
        """
            For a given year gets
            1. highest temparature and day
            2. lowest temparature and day
            3. most humidity and day

            return a required data in json format
        """

        done = self.prepare_dataframe_for_processing(year)
        if not done:
            return

        # fetching required rows out of dataframe
        max_temp_row = self.dataframe.  \
            loc[self.dataframe[MAX_TEMPC_COL].idxmax(
            )]
        min_temp_row = self.dataframe.  \
            loc[self.dataframe[MIN_TEMPC_COL].idxmin(
            )]
        max_humidity_row = self.dataframe.  \
            loc[self.dataframe[MAX_HUMIDITY_COL].idxmax(
            )]

        # Temparature stats for given Year
        data = {
            "temp": {
                "min": min_temp_row[MIN_TEMPC_COL],
                "minDay": min_temp_row[DATE_COL],
                "max": max_temp_row[MAX_TEMPC_COL],
                "maxDay": max_temp_row[DATE_COL],
            },
            "humidity": {
                "max": max_humidity_row[MAX_HUMIDITY_COL],
                "maxDay": max_humidity_row[DATE_COL]
            }
        }

        return data

    def get_monthly_stats(self, month):
        """
            For a given month of year gets
            1. average highest temparature
            2. average lowest temparature
            3. average humidity

            return a required data in json format
        """
        done = self.prepare_dataframe_for_processing(month)
        if not done:
            return

        # fetching required rows out of dataframe
        avg_max_temp = self.dataframe[MAX_TEMPC_COL].mean()
        avg_min_temp = self.dataframe[MIN_TEMPC_COL].mean()
        avg_mean_humidity = self.dataframe[MEAN_HUMIDITY_COL].mean()

        data = {
            "avg_max_temp": avg_max_temp,
            "avg_min_temp": avg_min_temp,
            "avg_max_humidity": avg_mean_humidity,
        }

        return data

    def prepare_dataframe_for_processing(self, key):
        """
        key: str refers to either year or month
           1. Check if there exists file paths for given key
           2. Get the dataframe from multiple files
           3. Preprocess the dataframe by filtering unwanted data

           returns bool
        """
        if not self.weather_files_dict.get(key):
            return False

        file_paths = self.weather_files_dict[key]
        self.dataframe = self.get_dataframe_from_files(file_paths)
        self.preprocess_dataframe()

        return True
