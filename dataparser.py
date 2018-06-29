import weatherdata
import os
import datetime
import csv


class DataParser:
    """Class for parsing and storing data in correct formats,
    this class is not static so multiple instances of data
    can be created and different changes can be made to them
    """
    def __init__(self):
        self.data = []

    @staticmethod
    def _get_oneday_data(line):
        """This function gets the raw data and populates the
        data structure with proper formatted data types and values"""
        daily_report = dict()

        for key in line.keys():
            if key == "PKT" or key == "PKST":
                date = line["PKT" if "PKT" == key else "PKST"].split("-")
                # Storing date in proper datetime format
                value = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                daily_report["PKT"] = value
            else:
                # Converting int/float values to their respective data types
                try:
                    value = int(line[key])
                except ValueError:
                    try:
                        value = float(line[key])
                    except ValueError:
                        value = "NA"

                daily_report[key.strip()] = value

        return daily_report

    def get_data(self, file_path):
        """This function reads data from all the txt
        files present in directory"""
        try:
            # Create a list of all the files to read
            all_files = [x for x in os.listdir(file_path) if x[-4:] == '.txt']
        except FileNotFoundError:
            print("Wrong path, no such directory exists!")
            return None

        for file_name in all_files:

            with open(file_path + "/" + file_name, "r") as weather_file:
                # Store the first row of the file for further use
                # with remaining rows.
                csv_file = csv.DictReader(weather_file, delimiter=",")

                for line in csv_file:
                    one_day_data = DataParser._get_oneday_data(line)

                    weather_data = weatherdata.WeatherData("NA", "NA", "NA",
                                                           "NA", "NA", "NA")
                    weather_data.date = one_day_data["PKT"]
                    weather_data.highest_temperature = one_day_data[
                        "Max TemperatureC"
                    ]
                    weather_data.lowest_temperature = one_day_data[
                        "Min TemperatureC"
                    ]
                    weather_data.mean_temperature = one_day_data[
                        "Mean TemperatureC"
                    ]
                    weather_data.max_humidity = one_day_data["Max Humidity"]
                    weather_data.mean_humidity = one_day_data["Min Humidity"]

                    self.data.append(weather_data)

        return self.data
