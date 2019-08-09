import csv

import dayinformation


def parse(files_dir, files):
    weather_readings = []

    for file in files:
        with open(files_dir + file) as f:
            reader = csv.DictReader(f)

            for row in reader:
                date = row['PKT']
                max_temp = row['Max TemperatureC']
                min_temp = row['Min TemperatureC']
                mean_humidity = row[' Mean Humidity']
                if max_temp != '' and min_temp != '' and mean_humidity != '':
                    weather_readings.append(dayinformation.DayInformation(date,
                                                                          int(max_temp),
                                                                          int(min_temp),
                                                                          int(mean_humidity)))

    return weather_readings