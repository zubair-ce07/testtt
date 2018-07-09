import traceback
import os
import csv
from weather_record import WeatherRecord


class ParsedWeatherReading:
    def __init__(self):
        self.weather_records = []

    def get_weather_records(self, weather_files_path, year, month=""):
        try:
            weather_files = [x for x in os.listdir(weather_files_path) if x[-4:] == '.txt'
                             and str(year) == x[-12:-8] and month in x[-7:-4]]
        except FileNotFoundError:
            traceback.print_exc()
        else:
            for weather_file_name in weather_files:
                with open(weather_files_path + "/" + weather_file_name, "r") as weather_file:
                    weather_reading_csv = csv.DictReader(weather_file, delimiter=",")

                    for weather_record_row in weather_reading_csv:
                        if not all([weather_record_row["Max TemperatureC"],
                                    weather_record_row["Min TemperatureC"],
                                    weather_record_row["Mean TemperatureC"],
                                    weather_record_row["Max Humidity"],
                                    weather_record_row[" Min Humidity"]]):
                            continue

                        weather_record = WeatherRecord(
                            weather_record_row.get("PKT", weather_record_row.get("PKST", None)),
                            weather_record_row["Max TemperatureC"],
                            weather_record_row["Min TemperatureC"],
                            weather_record_row["Mean TemperatureC"],
                            weather_record_row["Max Humidity"],
                            weather_record_row[" Min Humidity"],
                        )
                        self.weather_records.append(weather_record)

        if self.weather_records:
            return self.weather_records

        raise EOFError("No Record Exists for the given date")
