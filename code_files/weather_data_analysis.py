#!/usr/bin/python3.6
import calendar
import datetime

from read_weather import ReadWeather


class WeatherDataAnalysis:
    def calculate_yearly_report(self, weather_records, date):
        date_values = weather_records.year_attribute_readings('pkt', date)
        max_humidity_values = weather_records.year_attribute_readings('max_humidity', date)
        max_temperature_values = weather_records.year_attribute_readings('max_temperature', date)
        min_temperature_values = weather_records.year_attribute_readings('min_temperature', date)
        
        if not max_temperature_values:
            return None
        
        max_humidity = max(list(filter(None, max_humidity_values)))
        max_temperature = max(list(filter(None, max_temperature_values)))
        min_temperature = min(list(filter(None, min_temperature_values)))
        
        return {
            'highest_humidity': max_humidity,
            'lowest_temperature': min_temperature,
            'highest_temperature': max_temperature,
            'highest_humidity_date': date_values[max_humidity_values.index(max_humidity)],
            'lowest_temperature_date': date_values[min_temperature_values.index(min_temperature)],
            'highest_temperature_date': date_values[max_temperature_values.index(max_temperature)],
        }
        
    def calculate_monthly_report(self, weather_records, date):
        month_record = weather_records.month_readings(date)
        if not month_record:
            return None

        max_temperature_values = month_record.get('max_temperature')
        min_temperature_values = month_record.get('min_temperature')
        mean_humidity_values = month_record.get('mean_humidity')

        max_temperature_sum = sum(filter(None, max_temperature_values))
        min_temperature_sum = sum(filter(None, min_temperature_values))
        mean_humidity_sum = sum(filter(None, mean_humidity_values))

        total_max_temp_records = float(len(list(filter(None, max_temperature_values))))
        total_min_temp_records = float(len(list(filter(None, min_temperature_values))))
        total_mean_humidity_records = float(len(list(filter(None, mean_humidity_values))))
        
        return {
            'average_max_temperature': (max_temperature_sum / total_max_temp_records),
            'average_min_temperature': (min_temperature_sum / total_min_temp_records),
            'average_mean_humidity': (mean_humidity_sum / total_mean_humidity_records)
        }
