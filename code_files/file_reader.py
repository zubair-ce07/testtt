import csv

from weather_record import WeatherRecord


def read_weather_data(files):
    """
    Reads from a list of files and populates returns a
    populated weather structure for that month
    """
    daily_records = []

    for file_name in files:
        with open(file_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            daily_records += [WeatherRecord(record) for record in reader if is_record_valid(record)]

    return daily_records


def is_record_valid(record):
    required_fields = [record.get('Max TemperatureC'), record.get('Min TemperatureC'),
                       record.get('Max Humidity'), record.get(' Mean Humidity')]
    return all(required_fields)
