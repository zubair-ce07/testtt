#!/usr/bin/python3.6
import calendar

from read_weather import ReadWeather


class WeatherReadings:
    def __init__(self):
        self.weather_records = {}
    
    def add_month(self, month):
        date = month.file_data.get('pkt')[0]
        
        if self.weather_records.get(str(date.year)):
            self.weather_records[str(date.year)][str(date.month)] = month.file_data
        else:
            self.weather_records[str(date.year)] = {str(date.month): month.file_data}
    
    def year_attribute_readings(self, attribute, date):
        year_records = self.weather_records.get(str(date.year))
        if year_records:
            return [date_value for month in year_records for date_value in year_records[month][attribute]]
        return None

    def month_readings(self, date):
        year_records = self.weather_records.get(str(date.year))
        return year_records.get(str(date.month)) if year_records else None

    def months_name(self, month):
        return calendar.month_name[month.get('PKT')[0].month]

    def months_data_of_year(self, year):
        return self.weather_records.get(year)
