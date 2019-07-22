from os import listdir
from os.path import isfile, join
import pandas as pd
from pprint import pprint

MIN_TEMPC_COL = "Min TemperatureC"
MAX_TEMPC_COL = "Max TemperatureC"
MAX_HUMIDITY_COL = "Max Humidity"
DATE_COL = "PKST" # TODO: DATE_COL can have multiple names like PKST or PKT


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
            print("Reading from file", file_path)
            df = pd.read_csv(file_path, index_col=None, engine="python")
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
        if not self.weather_files_dict[year]:
            return
        
        file_paths = self.weather_files_dict[year]
        self.dataframe = self.get_dataframe_from_files(file_paths)
        self.preprocess_dataframe()

        # fetching required rows out of dataframe
        max_temp_row = self.dataframe.loc[self.dataframe[MAX_TEMPC_COL].idxmax()]
        min_temp_row = self.dataframe.loc[self.dataframe[MIN_TEMPC_COL].idxmin()]
        max_humidity_row = self.dataframe.loc[self.dataframe[MAX_HUMIDITY_COL].idxmax()]

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

        print(f'Highest: {data["temp"]["max"]}C on {data["temp"]["maxDay"]}')
        print(f'Lowest: {data["temp"]["min"]}C on {data["temp"]["minDay"]}')
        print(f'Humid: {data["humidity"]["max"]}% on {data["temp"]["maxDay"]}')

if __name__ == "__main__":
    # getting directory
    data_dir = 'weatherfiles/weatherfiles/'
    report = Report(data_dir)
    report.yearlyReport('2008')
    # FIXME: for data where date column is PKT rather than PKST
    