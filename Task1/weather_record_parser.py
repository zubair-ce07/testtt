import traceback
import os
import csv

from weather_record import WeatherRecord


class WeatherDataParser:

    required_fields = ["Max TemperatureC", "Min TemperatureC", "Mean TemperatureC",
                       "Max Humidity", " Min Humidity"]

    def __init__(self):
        self.weather_records = []

    def parse(self, files_path, year, month=None):
        files = [x for x in os.listdir(files_path) if x.endswith('.txt')]

        for file_name in files:
            with open(os.path.join(files_path, file_name), "r") as weather_file:
                weather_readings = csv.DictReader(weather_file, delimiter=",")

                for weather_record_row in weather_readings:
                    if all(weather_record_row.get(f) for f in WeatherDataParser.required_fields):
                        weather_record = WeatherRecord(
                            weather_record_row.get("PKT", weather_record_row.get("PKST", None)),
                            weather_record_row["Max TemperatureC"],
                            weather_record_row["Min TemperatureC"],
                            weather_record_row["Mean TemperatureC"],
                            weather_record_row["Max Humidity"],
                            weather_record_row[" Min Humidity"],
                        )

                        if (weather_record.date.month == month if month else True) \
                                and weather_record.date.year == year:
                            self.weather_records.append(weather_record)

        if not self.weather_records:
            raise EOFError("No Record Exists for the given date")

        return self.weather_records
