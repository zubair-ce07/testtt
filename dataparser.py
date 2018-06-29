import weatherdata
import os
import datetime


class DataParser:
    """Class for parsing and storing data in correct formats,
    this class is not static so multiple instances of data
    can be created and different changes can be made to them
    """
    def __init__(self):
        self.data = []

    @staticmethod
    def _get_oneday_data(day_report, header):
        """This function gets the raw data and populates the
        data structure with proper formatted data types and values"""
        daily_report = dict()

        for idx, value in enumerate(day_report.split(",")):
            if idx == 0:
                date = value.split("-")
                # Storing date in proper datetime format
                value = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            else:
                # Converting int/float values to their respective data types
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        value = "NA"
            # Keeping the key for date consistent
            date_key = "PKT" if header[idx].strip() == "PKST" \
                else header[idx].strip()
            daily_report[date_key] = value
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
            try:
                file = open(file_path + "/" + file_name, "r")
                # Store the first row of the file for further use
                # with remaining rows.
                header = file.readline().split(",")

                for line in file:
                    oneday_data = DataParser._get_oneday_data(line, header)

                    weather_data = weatherdata.WeatherData("NA", "NA", "NA",
                                                           "NA", "NA", "NA")
                    weather_data.date = oneday_data["PKT"]
                    weather_data.highest_temperature = oneday_data[
                        "Max TemperatureC"
                    ]
                    weather_data.lowest_temperature = oneday_data[
                        "Min TemperatureC"
                    ]
                    weather_data.mean_temperature = oneday_data[
                        "Mean TemperatureC"
                    ]
                    weather_data.max_humidity = oneday_data["Max Humidity"]
                    weather_data.mean_humidity = oneday_data["Min Humidity"]

                    self.data.append(weather_data)

                file.close()
            except FileNotFoundError:
                print("Wrong file path or name, no such file exists!")
                return None

        return self.data
