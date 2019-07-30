#!/usr/bin/python3
from operator import attrgetter

from weather_results import WeatherResults


class WeatherAnalyzer:
    def __init__(self, weather_records):
        self.weather_records = weather_records

    def get_yearly_temperature_peaks(self):
        
        seq = [max(self.weather_records[i], key=attrgetter('max_temprature')) \
                for i in range(len(self.weather_records))]
        max_temprature = max(seq, key=attrgetter('max_temprature'))

        seq = [min(self.weather_records[i], key=attrgetter('min_temprature')) \
                for i in range(len(self.weather_records))]
        min_temprature = min(seq, key=attrgetter('min_temprature'))

        seq = [max(self.weather_records[i], key=attrgetter('max_humidity')) \
                for i in range(len(self.weather_records))]
        max_humidity = max(seq, key=attrgetter('max_humidity'))

        result = WeatherResults(
            max_temprature=max_temprature,
            min_temprature=min_temprature,
            max_humidity=max_humidity
        )
        return result

    def get_monthly_avg_results(self):

        __sum = sum(c.max_temprature for c in self.weather_records)
        highest_avg_temp = int(__sum/len(self.weather_records))

        __sum = sum(c.min_temprature for c in self.weather_records)
        lowest_avg_temp = int(__sum/len(self.weather_records))

        __sum = sum(c.mean_humidity for c in self.weather_records)
        avg_mean_humidity = int(__sum/len(self.weather_records))

        result = WeatherResults(
            highest_avg_temp=highest_avg_temp,
            lowest_avg_temp=lowest_avg_temp,
            avg_mean_humidity=avg_mean_humidity
        )

        return result
