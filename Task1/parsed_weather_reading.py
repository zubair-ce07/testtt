import traceback
import os
import csv

from weather_record import WeatherRecord


class ParsedWeatherReading:

    required_fields = ["Max TemperatureC", "Min TemperatureC", "Mean TemperatureC",
                       "Max Humidity", " Min Humidity"]

    def __init__(self):
        self.weather_records = []

    def get_weather_records(self, weather_files_path, year, month=None):
        try:
            weather_files = [x for x in os.listdir(weather_files_path) if x[-4:] == '.txt']
        except FileNotFoundError:
            traceback.print_exc()
        else:
            for weather_file_name in weather_files:
                with open(os.path.join(weather_files_path, weather_file_name), "r") as weather_file:
                    weather_reading_csv = csv.DictReader(weather_file, delimiter=",")

                    for weather_record_row in weather_reading_csv:
                        if all(weather_record_row.get(f) for f in ParsedWeatherReading.required_fields):
                            weather_record = WeatherRecord(
                                weather_record_row.get("PKT", weather_record_row.get("PKST", None)),
                                weather_record_row["Max TemperatureC"],
                                weather_record_row["Min TemperatureC"],
                                weather_record_row["Mean TemperatureC"],
                                weather_record_row["Max Humidity"],
                                weather_record_row[" Min Humidity"],
                            )

                            if (weather_record.weather_record_date.month == month if month else True) \
                                    and weather_record.weather_record_date.year == year:
                                self.weather_records.append(weather_record)

        if self.weather_records:
            return self.weather_records

        raise EOFError("No Record Exists for the given date")
