import csv

import dayinformation


def reader(files_dir, files):
    weather_readings = []

    for file in files:
        with open(files_dir + file) as f:
            dict_reader = csv.DictReader(f)

            for row in dict_reader:
                date = row.get('PKT', row.get('PKST', None))
                max_temp = row['Max TemperatureC']
                min_temp = row['Min TemperatureC']
                mean_humidity = row[' Mean Humidity']
                if all((max_temp != '', min_temp != '', mean_humidity != '')):
                    weather_readings.append(dayinformation.DayInformation(date,
                                                                          int(max_temp),
                                                                          int(min_temp),
                                                                          int(mean_humidity)))

    return weather_readings
