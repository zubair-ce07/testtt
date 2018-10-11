import csv
from glob import glob

from data_holder import WeatherData


class WeatherCalculations:
    '''
    This class perform calculation to create weather report
    '''

    def highest_temp_record(self, weather_records):
        '''
        This method takes list of WeatherData and return data having max_temp.
        '''
        return max(weather_records, key=lambda day: day.max_temp)

    def lowest_temp_record(self, weather_records):
        '''
        This method takes list of WeatherData and return data having min_temp.
        '''
        return min(weather_records, key=lambda day: day.max_temp)

    def highest_humidity_record(self, weather_records):
        '''
        This method takes list of WeatherData and return data having maximum
        mean_humidity.
        '''
        return max(weather_records, key=lambda day: day.mean_humidity)

    def average_max_temp(self, weather_records):
        '''
        This method take list of WeatherData and return mean of max_temp.
        '''
        max_temp_values = [day.max_temp for day in weather_records]
        return sum(max_temp_values) // len(max_temp_values)

    def average_min_temp(self, weather_records):
        '''
        This method take list of WeatherData and return mean of min_temp.
        '''
        min_temp_values = [day.min_temp for day in weather_records]
        return sum(min_temp_values) // len(min_temp_values)

    def average_mean_humidity(self, weather_records):
        '''
        This method take list of WeatherData and return mean of mean_humidity.
        '''
        mean_humdity_values = [day.mean_humidity for day in weather_records]
        return sum(mean_humdity_values) // len(mean_humdity_values)

    def all_weather_record(self, dir_path):
        '''
        This method directory path and return read all txt files.
        '''
        weather_records = []
        for file_name in glob(f'{dir_path}*.txt'):
            with open(file_name ) as data_file:
                weather_records += [WeatherData(row) for row in csv.DictReader(data_file) if self.is_valid(row)]
        return weather_records

    def is_valid(self, weather_record):
        required_data = [weather_record.get('Max TemperatureC'),
                         weather_record.get('Min TemperatureC'),
                         weather_record.get(' Mean Humidity'),
                         weather_record.get('PKT') or weather_record.get('PKST')]
        if all(required_data):
            return True
        return False

    def month_records(self, weather_records, req_date):
        return [day for day in weather_records if day.date.year == req_date.year and day.date.month == req_date.month]

    def year_report(self, weather_records, req_date):
        req_records = [day for day in weather_records if day.date.year == req_date.year]
        if not req_records:
            return
        return self.highest_temp_record(req_records), self.lowest_temp_record(
            req_records), self.highest_humidity_record(req_records)

    def average_report(self, waether_records, req_date):
        req_records = self.month_records(waether_records, req_date)
        if not req_records:
            return
        return self.average_max_temp(req_records), self.average_min_temp(
            req_records), self.average_mean_humidity(req_records)
