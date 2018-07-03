import datetime
import traceback
import weather_dataset
import os
import csv


class ParsedWeatherData:
    required_readings = [
        "PKT", "PKST", "Max TemperatureC", "Min TemperatureC",
        "Mean TemperatureC", "Max Humidity", "Min Humidity"
    ]

    def __init__(self):
        self.data = []
        self.keys = []

    def get_filtered_data(self, file_path, year, month=""):
        try:
            all_files = [x for x in os.listdir(file_path) if x[-4:] == '.txt'
                         and str(year) in x and month in x]
        except FileNotFoundError:
            traceback.print_exc()
        else:
            for file_name in all_files:
                with open(file_path + "/" + file_name, "r") as weather_file:
                    csv_file = csv.DictReader(weather_file, delimiter=",")

                    for line in csv_file:
                        daily_data = dict()
                        keys = [key for key in line.keys() if key.strip() in ParsedWeatherData.required_readings]

                        for key in keys:
                            if key == "PKT" or key == "PKST":
                                date = line["PKT" if "PKT" == key else "PKST"].split("-")
                                value = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                                daily_data["PKT"] = value
                            else:
                                try:
                                    value = int(line[key])
                                except ValueError:
                                    try:
                                        value = float(line[key])
                                    except ValueError:
                                        value = "NA"

                                daily_data[key.strip()] = value

                        weather_data = weather_dataset.WeatherData(
                            daily_data["PKT"], daily_data["Max TemperatureC"], daily_data["Min TemperatureC"],
                            daily_data["Mean TemperatureC"], daily_data["Max Humidity"], daily_data["Min Humidity"]
                        )

                        self.data.append(weather_data)

        return self.data
