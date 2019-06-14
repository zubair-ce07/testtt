import csv
import os

from weather_record import WeatherRecord


class DataSetCollector:

    def collect_files(self, files_path):
        """collects all datasets files"""
        weather_files_record = []
        for file_name in os.listdir(files_path):
            if not file_name.startswith('.'):
                weather_files_record.append(files_path + file_name)
        return weather_files_record

    def read_file_data(self, file_path):
        """Reads and return file data"""
        try:
            file_data = []
            with open(file_path) as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    file_data.append(row)
            return file_data
        except IOError:
            print("Error: can\'t find file or read data")
            exit()

    def read_files(self, files_path):
        """collects all the data set and saves in data structure"""
        weather_records = []
        weather_files_record = self.collect_files(files_path)
        for file in weather_files_record:
            file_data = self.read_file_data(file)
            for day_data in file_data:
                if len(day_data) > 2:
                    if self.check_valid_record_row(day_data) and \
                            day_data["Max TemperatureC"] and \
                            day_data["Min TemperatureC"] and \
                            day_data["Max Humidity"]:
                        weather_records.append(WeatherRecord(
                            self.get_day_date(day_data),
                            day_data["Max TemperatureC"],
                            day_data["Mean TemperatureC"],
                            day_data["Min TemperatureC"],
                            day_data["Dew PointC"], day_data["MeanDew PointC"],
                            day_data["Min DewpointC"],
                            day_data["Max Humidity"],
                            day_data[" Mean Humidity"],
                            day_data[" Min Humidity"],
                            day_data[" Max Sea Level PressurehPa"],
                            day_data[" Mean Sea Level PressurehPa"],
                            day_data[" Min Sea Level PressurehPa"],
                            day_data[" Max VisibilityKm"],
                            day_data[" Mean VisibilityKm"],
                            day_data[" Min VisibilitykM"],
                            day_data[" Max Wind SpeedKm/h"],
                            day_data[" Mean Wind SpeedKm/h"],
                            day_data[" Max Gust SpeedKm/h"],
                            day_data["Precipitationmm"],
                            day_data[" CloudCover"], day_data[" Events"],
                            day_data["WindDirDegrees"]
                        ))
        return weather_records

    def get_day_date(self, day_obj):
        if day_obj.get("PKT"):
            return day_obj["PKT"]
        return day_obj["PKST"]

    def check_valid_record_row(self, day_obj):
        if day_obj.get("PKT") != "PKT" or day_obj.get("PKST") != "PKST":
            return True
        return False
