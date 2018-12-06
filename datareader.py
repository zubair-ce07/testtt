import glob
import csv
from classes import WeatherInformation


def data_parser(path):
    files_data = glob.glob(path)
    weather_reading = []

    for item in files_data:
        with open(item, "r") as file_data:
            header = file_data.readline().split(',')
            header = [column.strip() for column in header]
            readings = csv.DictReader(file_data, fieldnames=header)

            for reading in readings:
                weather_information = WeatherInformation()
                weather_information.date = reading.get('PKST', reading.get('PKT', ''))
                weather_information.max_temp = reading.get('Max TemperatureC', '')
                weather_information.low_temp = reading.get('Min TemperatureC', '')
                weather_information.max_humid = reading.get('Max Humidity', '')
                weather_information.mean_humid = reading.get('Mean Humidity', '')
                weather_reading.append(weather_information)
    return weather_reading
