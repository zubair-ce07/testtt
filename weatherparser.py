import os.path
import csv


class WeatherParser:


    def read_weather_file(self, filepath):
        weather_fields = ['Max TemperatureC','Min TemperatureC','Max Humidity',' Mean Humidity']
        weather_readings = []
        if not os.path.exists(filepath):
            return False
        with open (filepath) as weatherfile:
            reader = csv.DictReader(weatherfile)
            for row in reader:
                if all(row.get(fields) for fields in weather_fields):
                    try:
                        weather_readings.append(tuple((row['PKT'], row['Max TemperatureC'],
                                                       row['Min TemperatureC'], row['Max Humidity'],
                                                       row[' Mean Humidity'])))
                    except KeyError as error:
                        weather_readings.append(tuple((row['PKST'], row['Max TemperatureC'],
                                                       row['Min TemperatureC'], row['Max Humidity'],
                                                       row[' Mean Humidity'])))
        return weather_readings
