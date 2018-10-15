import csv
from glob import glob

from weather_records import WeatherRecord


class WeatherCalculations:
    """
    This class perform calculation to create weather report
    """

    def read_weather_records(self, dir_path):
        """
        This method directory path and return read all txt files.
        """
        weather_records = []
        for file_name in glob(f'{dir_path}*.txt'):
            with open(file_name) as data_file:
                weather_records += [WeatherRecord(row) for row in csv.DictReader(data_file) if self.is_valid(row)]
        return weather_records

    def is_valid(self, weather_record):
        required_data = [weather_record.get('Max TemperatureC'),
                         weather_record.get('Min TemperatureC'),
                         weather_record.get(' Mean Humidity'),
                         weather_record.get('PKT') or weather_record.get('PKST')]
        return all(required_data)

    def month_records(self, weather_records, req_date):
        return [day for day in weather_records if day.date.year == req_date.year and day.date.month == req_date.month]

    def year_report(self, weather_records, req_date):
        req_records = [day for day in weather_records if day.date.year == req_date.year]
        if not req_records:
            return

        highest_temperature_record = max(req_records, key=lambda day: day.max_temp)
        lowest_temperature_record = min(req_records, key=lambda day: day.max_temp)
        highest_humidity_record = max(req_records, key=lambda day: day.mean_humidity)

        return highest_temperature_record, lowest_temperature_record, highest_humidity_record

    def average_report(self, weather_records, req_date):
        req_records = self.month_records(weather_records, req_date)
        if not req_records:
            return

        average_max_temperature = sum([day.max_temp for day in req_records]) // len(req_records)
        average_min_temperature = sum([day.min_temp for day in req_records]) // len(req_records)
        average_mean_humidity = sum([day.mean_humidity for day in req_records]) // len(req_records)

        return average_max_temperature, average_min_temperature, average_mean_humidity
