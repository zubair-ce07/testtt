import copy
import csv
from data import data


class read_file:
    def read_file(file_names, day_record, weather_data):
        day_record.clear()
        for data in file_names:
            with open(data, "r") as csvFile:
                reader = csv.reader(csvFile)
                next(reader)
                for data in reader:
                    weather_data.update([('PKT', data[0]),
                                         ('Max TemperatureC',
                                          data[1]), ('Min TemperatureC', data[3]),
                                         ('Max Humidity', data[7]),
                                         ('Mean Humidity',
                                          data[8])])
                    day_record.append(copy.deepcopy(weather_data))
            csvFile.close()

