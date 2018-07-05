import traceback
import os
import csv
import datetime
import weather_recordset


class ParsedWeatherReading:
    def __init__(self):
        self.weather_records = []

    def get_weather_records(self, weather_files_path, year, month=""):
        try:
            # Getting only files for which year and month has been specified.
            weather_files = [x for x in os.listdir(weather_files_path) if x[-4:] == '.txt'
                             and str(year) == x[-12:-8] and month in x[-7:-4]]
        except FileNotFoundError:
            traceback.print_exc()
        else:
            for weather_file_name in weather_files:
                with open(weather_files_path + "/" + weather_file_name, "r") as weather_file:
                    weather_reading_csv = csv.DictReader(weather_file, delimiter=",")

                    # In the loop below we are getting actual key values from weather_record_row dict
                    # for handling inconsistent leading or trailing spaces.
                    for weather_record_row in weather_reading_csv:
                        weather_date = weather_record_row["PKT" if "PKT" in weather_record_row.keys()
                                                          else "PKST"].split("-")
                        max_temperature = weather_record_row[[key for key in weather_record_row.keys()
                                                              if key.strip() == "Max TemperatureC"][0]]
                        min_temperature = weather_record_row[[key for key in weather_record_row.keys()
                                                              if key.strip() == "Min TemperatureC"][0]]
                        mean_temperature = weather_record_row[[key for key in weather_record_row.keys()
                                                               if key.strip() == "Mean TemperatureC"][0]]
                        max_humidity = weather_record_row[[key for key in weather_record_row.keys()
                                                           if key.strip() == "Max Humidity"][0]]
                        min_humidity = weather_record_row[[key for key in weather_record_row.keys()
                                                           if key.strip() == "Min Humidity"][0]]

                        weather_record = weather_recordset.WeatherRecord(
                            datetime.date(int(weather_date[0]), int(weather_date[1]), int(weather_date[1])),
                            int(max_temperature) if max_temperature != "" else "",
                            int(min_temperature) if min_temperature != "" else "",
                            float(mean_temperature) if mean_temperature != "" else "",
                            float(max_humidity) if max_humidity != "" else "",
                            float(min_humidity) if min_humidity != "" else "",
                        )
                        self.weather_records.append(weather_record)

        if self.weather_records:
            return self.weather_records
        else:
            print("No Record Exists for the given date")
