#!/usr/bin/python3
from weather_results import WeatherResults


class ResultCalculator:
    def __init__(self, monthly_weather_records, yearly_weather_records):
        self.monthly_weather_records = monthly_weather_records
        self.yearly_weather_records = yearly_weather_records

    def get_yearly_temperature_peaks(self):
        result = WeatherResults()
        result.max_temprature = self.yearly_weather_records[0][0]
        result.min_temprature = self.yearly_weather_records[0][0]
        result.max_humidity = self.yearly_weather_records[0][0]
        for monthly_record in self.yearly_weather_records:
            for daily_record in monthly_record:
                if result.max_temprature.max_temprature < daily_record.max_temprature:
                    result.max_temprature = daily_record
                if result.min_temprature.min_temprature > daily_record.min_temprature:
                    result.min_temprature = daily_record
                if result.max_humidity.max_humidity < daily_record.max_humidity:
                    result.max_humidity = daily_record
        return result

    def get_monthly_avg_results(self):
        result = WeatherResults()
        result.max_avg_temperature = 0
        result.min_avg_temperature = 0
        result.mean_humidity_avg = 0

        for daily_record in self.monthly_weather_records:
            result.max_avg_temperature += daily_record.max_temprature
            result.min_avg_temperature += daily_record.min_temprature
            result.mean_humidity_avg += daily_record.mean_humidity
        row_count = len(self.monthly_weather_records)
        result.max_avg_temperature /= row_count
        result.min_avg_temperature /= row_count
        result.mean_humidity_avg /= row_count
        return result
