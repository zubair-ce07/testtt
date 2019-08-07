import copy
import csv
from data import data


class ReadFile:

    def read_file(file_names, day_record, weather_data):

        day_record.clear()

        for data in file_names:
            
            with open(data, "r") as csvFile:
                reader = csv.DictReader(csvFile)

                for data_read in reader:
                    try:
                        weather_data["PKT"] = data_read["PKT"]
                    except:
                        weather_data["PKT"] = data_read["PKST"]
                    weather_data["Max TemperatureC"] = data_read["Max TemperatureC"]
                    weather_data["Min TemperatureC"] = data_read["Min TemperatureC"]
                    weather_data["Max Humidity"] = data_read["Max Humidity"]
                    weather_data["Mean Humidity"] = data_read[" Mean Humidity"]

                    if weather_data['PKT'] != '' and weather_data['Max TemperatureC'] != '' and weather_data['Min TemperatureC'] != '' and weather_data['Mean Humidity'] != ''and weather_data['Max TemperatureC'] != '':
                        day_record.append(copy.deepcopy(weather_data))

            csvFile.close()

