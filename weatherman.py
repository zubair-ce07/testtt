from os import listdir
from os.path import isfile, join, isdir
import pandas as pd
from pprint import pprint
import click
from datetime import datetime
from termcolor import colored

MIN_TEMPC_COL = "Min TemperatureC"
MAX_TEMPC_COL = "Max TemperatureC"
MAX_HUMIDITY_COL = "Max Humidity"
MEAN_HUMIDITY_COL = "Mean Humidity"
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
        #   if file_year not in self.weather_files_dict:
        #             month = f.split('_')[-1]
        #             self.weather_files_dict[file_year] = {month: file_path}
        #         else:
        #             self.weather_files_dict[file_year].update(
        #                 {month: file_path}
        for f in listdir(dir_path):
            file_path = join(dir_path, f)
            if isfile(file_path):
                file_year = f.split('_')[-2]
                if file_year not in self.weather_files_dict:
                    self.weather_files_dict[file_year] = [file_path]
                else:
                    self.weather_files_dict[file_year].append(file_path)

    def process_files_for_month(self, dir_path, year):
        """
            process the given directory for weather files and store the files path
            in a dictionary for later processing

            weather_files_dict = { month : list of file paths of given year}
        """
        for f in listdir(dir_path):
            file_path = join(dir_path, f)
            if isfile(file_path):
                file_year = f.split('_')[-2]
                if file_year != year:
                    continue

                month = f.split('_')[-1]
                month = month.split('.')[0]
                if month not in self.weather_files_dict:
                    self.weather_files_dict[month] = [file_path]
                else:
                    self.weather_files_dict[month].append(file_path)

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

        self.prepare_dataframe_for_processing(year)

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

    def get_monthly_stats(self, month):
        """
            For a given month of year gets
            1. average highest temparature
            2. average lowest temparature
            3. average humidity

            return a required data in json format
        """
        self.prepare_dataframe_for_processing(month)

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
        key:str refers to either year or month
           1. Check if there exists file paths for given key
           2. Get the dataframe from multiple files
           3. Preprocess the dataframe by filtering unwanted data
        """
        if not self.weather_files_dict.get(key):
            return

        file_paths = self.weather_files_dict[key]
        self.dataframe = self.get_dataframe_from_files(file_paths)
        self.preprocess_dataframe()


class Report:
    def __init__(self, dir_path):
        self.wm = WeatherMan()
        self.data_dir = dir_path

    def monthly_report(self, year, month):
        self.wm.process_files_for_month(self.data_dir, year)
        monthlyData = self.wm.get_monthly_stats(month)
        self.print_monthly_report(monthlyData)

    def yearly_report(self, year):
        self.wm.process_files(self.data_dir)
        yearlyData = self.wm.get_year_stats(year)
        self.print_yearly_report(yearlyData)

    def monthly_horizontal_chart(self, year, month, single_line):
        self.wm.process_files_for_month(self.data_dir, year)
        self.wm.prepare_dataframe_for_processing(month)
        self.print_monthly_horizontal_chart(single_line)

    def format_date(self, date):
        """
            gets date in a format yyyy-mm-dd
        """
        year = int(date.split("-")[0])
        month = int(date.split("-")[1])
        day = int(date.split("-")[2])

        return datetime(year, month, day).strftime("%b %d")

    def print_yearly_report(self, data):
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

        print("Humid: %d on %s" %
              (
                  data["humidity"]["max"],
                  self.format_date(data["humidity"]["maxDay"]))
              )

    def print_monthly_report(self, data):
        """
            data type : json
            data schema: {
                "avg_max_temp": avg_max_temp,
                "avg_min_temp": avg_min_temp,
                "avg_max_humidity": avg_max_humidity,
            }
        """
        if data is None:
            print("Data not found for given month of the year")
            return

        print("Highest Average: %dC" % (data["avg_max_temp"]))
        print("Lowest Average: %dC" % (data["avg_min_temp"]))
        print("Average Humidity: %d%%" % (data["avg_max_humidity"]))

    def draw_horizontal_bar(self, day, min, max, single_line):
        bar = '+'
        if single_line:
            print(
                day,
                colored(bar * min, 'blue') + colored(bar * max, 'red'),
                str(min) + "C - " + str(max) + "C"
            )
            return

        print(day, colored(bar * max, 'red'), str(max)+"C")
        print(day, colored(bar * min, 'blue'), str(min)+"C")

    def print_monthly_horizontal_chart(self, single_line):
        df = self.wm.dataframe
        # Droping rows where min, max temp is NAN
        df = df[df[MAX_TEMPC_COL].notnull() & df[MIN_TEMPC_COL].notnull()]
        for index, row in df.iterrows():
            self.draw_horizontal_bar(
                index,
                int(row[MIN_TEMPC_COL]),
                int(row[MAX_TEMPC_COL]),
                single_line
            )


def get_month_and_year(data):
    month_splitter = '/'
    if(len(data.split(month_splitter)) != 2):
        print("Provided data is invalid. use --help for more details.")
        return

    num_to_month = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }

    year = data.split(month_splitter)[0]
    month = data.split(month_splitter)[1]
    month = num_to_month.get(int(month))

    if month is None:
        print("Provided month is invalid.")
        return

    return (year, month)


@click.command()
@click.option(
    '-e',
    nargs=1,
    help="gets an year in format yyyy. Prints the stats for most humdity, "
    "lowest temparature, and "
    "highest temparture for the given year."


)
@click.option(
    '-a',
    nargs=1,
    help="gets date in format yyyy/mm. Prints the average stats for humdity, "
    "lowest temparature, and highest temparture for the given month of the year."
)
@click.option(
    '-c',
    nargs=1,
    help="gets date in format yyyy/mm. Prints a horizontal bar chart for each day for, "
    "lowest temparature, and highest temparture"
)
@click.argument('path_to_files')
@click.option(
    '-multiple',
    default="1",
    nargs=0,
    help="displays a single line horizontal bar chart. Use this tag with -c.\n"
    "use 1 for single line. "
    "and 0 for multiple line"
)
def argumentParser(e, a, c, path_to_files, multiple):
    if not isdir(path_to_files):
        print("File path of data directory is invalid.")
        return

    if e:
        report = Report(path_to_files)
        report.yearly_report(e)
        return

    if a:
        year, month = get_month_and_year(a)
        report = Report(path_to_files)
        report.monthly_report(year, month)
        return

    if c:
        year, month = get_month_and_year(c)
        report = Report(path_to_files)

        if not multiple:
            report.monthly_horizontal_chart(year, month, single_line=False)
        else:
            report.monthly_horizontal_chart(year, month, single_line=True)

        return


if __name__ == "__main__":
    argumentParser()
