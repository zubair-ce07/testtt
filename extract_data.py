import calendar
import collections
import csv
import glob

from weather_record import WeatherRecord


class ExtractData:
    def __init__(self):
        self.file_names = ""
        self.weather_records = []

    def get_file_names_yearly(self, files_dir, date_):
        header = []
        data_set = []
        self.file_names = glob.glob("{0}/*{1}*.txt".format(files_dir, date_))

    def get_file_names_monthly(self, files_dir, date_):
        year, month = date_.split("/")
        month_name_ = calendar.month_name[int(month)]
        month_name_ = month_name_[:3]
        sub_string = year + "_" + month_name_
        self.file_names = glob.glob("{0}/*{1}.txt".format(files_dir, sub_string))

    def read_data(self):

        for f in self.file_names:
            with open(f, 'rt') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    records = WeatherRecord()
                    records.load_weather_record(row["PKT"], row["Max TemperatureC"], row["Mean TemperatureC"],
                                                row["Min TemperatureC"], row["Dew PointC"], row["MeanDew PointC"],
                                                row["Min DewpointC"], row["Max Humidity"], row[" Mean Humidity"],
                                                row[" Min Humidity"], row[" Max Sea Level PressurehPa"],
                                                row[" Mean Sea Level PressurehPa"], row[" Min Sea Level PressurehPa"],
                                                row[" Max VisibilityKm"], row[" Mean VisibilityKm"],
                                                row[" Min VisibilitykM"], row[" Max Wind SpeedKm/h"],
                                                row[" Mean Wind SpeedKm/h"], row[" Max Gust SpeedKm/h"],
                                                row["Precipitationmm"], row[" CloudCover"], row[" Events"],
                                                row["WindDirDegrees"])
                    self.weather_records.append(records)

        return self.weather_records
