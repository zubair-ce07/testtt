from os import listdir
from os.path import isfile, join, isdir
import pandas as pd
from pprint import pprint
import click
from datetime import datetime

MIN_TEMPC_COL = "Min TemperatureC"
MAX_TEMPC_COL = "Max TemperatureC"
MAX_HUMIDITY_COL = "Max Humidity"
DATE_COL = "PKST"


class WeatherMan:
    weather_files_dict = {}
    dataframe = None

    def process_files(self, dir_path):
        """
            process the given directory for weather files and store the files path
            in a dictionary for later processing

            weather_files_dict = { year : list of file paths of given year}
        """
        for f in listdir(dir_path):
            file_path = join(dir_path, f)
            if isfile(file_path):
                file_year = f.split('_')[-2]
                if file_year not in self.weather_files_dict:
                    self.weather_files_dict[file_year] = [file_path]
                else:
                    self.weather_files_dict[file_year].append(file_path)

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

    def get_year_stats(self, year):
        """
            For a given year displays
            1. highest temparature and day
            2. lowest temparature and day
            3. most humidity and day

            return a required data in json format
        """

        if not self.weather_files_dict.get(year):
            return

        file_paths = self.weather_files_dict[year]
        self.dataframe = self.get_dataframe_from_files(file_paths)
        self.preprocess_dataframe()

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

        data = {}
        # Temparature stats for given Year
        data["temp"] = {
            "min": min_temp_row[MIN_TEMPC_COL],
            "minDay": min_temp_row[DATE_COL],
            "max": max_temp_row[MAX_TEMPC_COL],
            "maxDay": max_temp_row[DATE_COL],
        }
        # Humidity Stats for given Year
        data["humidity"] = {
            "max": max_humidity_row[MAX_HUMIDITY_COL],
            "maxDay": max_humidity_row[DATE_COL]
        }

        return data


class Report:
    def __init__(self, dir_path):
        self.wm = WeatherMan()
        self.data_dir = dir_path

    def yearlyReport(self, year):
        self.wm.process_files(self.data_dir)
        yearlyData = self.wm.get_year_stats(year)
        self.printYearlyReport(yearlyData)

    def format_date(self, date):
        """
            gets date in a format yyyy-mm-dd
        """
        year = int(date.split("-")[0])
        month = int(date.split("-")[1])
        day = int(date.split("-")[2])

        return datetime(year, month, day).strftime("%b %d")

    def printYearlyReport(self, data):
        """
            data type : json
            data schema: {
                temp : {
                    min,
                    minDay,
                    max,
                    maxDay
                },
                humidity: {
                    max,
                    maxDay
                }
            }
        """
        if data is None:
            print("Data not found for year")
            return

        print("Highest: %dC on %s" %
              (data["temp"]["max"], self.format_date(data["temp"]["maxDay"])))

        print("Lowest: %dC on %s" %
              (data["temp"]["min"], self.format_date(data["temp"]["minDay"])))

        print("Humid: %dC on %s" %
              (
                  data["humidity"]["max"],
                  self.format_date(data["humidity"]["maxDay"]))
              )


@click.command()
@click.option(
    '-e',
    nargs=1,
    help="prints the stats for most humdity, "
    "lowest temparature, and"
    "highest temparture for the given year.")
@click.argument('path_to_files')
def argumentParser(e, path_to_files):
    if not isdir(path_to_files):
        print("File path of data directory is invalid.")
        return

    if(e):
        report = Report(path_to_files)
        report.yearlyReport(e)
        return


if __name__ == "__main__":
    argumentParser()
