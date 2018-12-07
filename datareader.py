import glob
import csv
from classes import WeatherRecord


def data_parser(path):
    weather_reading = []
    for f in glob.glob(path):
        readings = csv.DictReader(open(f))
        for reading in readings:
            reading = {k.strip():v for k,v in reading.items()}
            date = reading.get('PKST', reading.get('PKT'))
            max_temp = reading.get('Max TemperatureC')
            low_temp = reading.get('Min TemperatureC')
            max_humid = reading.get('Max Humidity')
            mean_humid = reading.get('Mean Humidity')

            if (date != '') & (max_temp != '') & (low_temp != '') & (max_humid != '') & (mean_humid != ''):
                weather_reading.append(WeatherRecord(date, int(max_temp), int(low_temp), max_humid, int(mean_humid)))

    return weather_reading
