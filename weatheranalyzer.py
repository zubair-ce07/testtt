from collections import namedtuple
from operator import attrgetter


class WeatherAnalyzer:

    def __init__(self, weather_readings):
        self.weather_readings = weather_readings

    def annual_extremes(self, date):
        AnnualResult = namedtuple('AnnualResult', ['max_temp_reading', 'min_temp_reading', 'max_humid_reading'])
        weather_readings = [reading for reading in self.weather_readings if reading.date.year == date.year]
        if weather_readings:
            return AnnualResult(
                max(weather_readings, key=attrgetter('max_temperature')),
                min(weather_readings, key=attrgetter('min_temperature')),
                max(weather_readings, key=attrgetter('max_humidity'))
            )

    def monthly_average(self, date):
        MonthlyResult = namedtuple('MonthlyResult', ['max_temp_avg', 'min_temp_avg', 'mean_humid_avg'])

        weather_readings = [reading for reading in self.weather_readings
                            if reading.date.year == date.year and reading.date.month == date.month]
        if weather_readings:
            max_temp_avg = sum([reading.max_temperature for reading in weather_readings]) / len(weather_readings)
            min_temp_avg = sum([reading.min_temperature for reading in weather_readings]) / len(weather_readings)
            mean_hum_avg = sum([reading.mean_humidity for reading in weather_readings]) / len(weather_readings)

            return MonthlyResult(max_temp_avg, min_temp_avg, mean_hum_avg)

    def filter_readings(self, date):
        return [reading for reading in self.weather_readings
                if reading.date.year == date.year and reading.date.month == date.month]
