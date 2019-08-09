import csv

import weatherrecord


def reader(files):
    weather_readings = []

    for file in files:
        with open(file) as f:
            dict_reader = csv.DictReader(f)

            for row in dict_reader:
                date = row.get('PKT', row.get('PKST'))
                max_temp = row.get('Max TemperatureC')
                min_temp = row.get('Min TemperatureC')
                mean_humidity = row.get(' Mean Humidity')
                if all((max_temp != '', min_temp != '', mean_humidity != '')):
                    weather_readings.append(weatherrecord.WeatherRecord(date, int(max_temp), int(min_temp),
                                                                        int(mean_humidity)))

    return weather_readings
