import re

from data_set_collector import DataSetCollector


class WeatherAnalyzer:
    def __init__(self):
        self.weather_data_set_records = []

    def collect_data_set(self, files_path):
        data_set_collector = DataSetCollector()
        self.weather_data_set_records = data_set_collector.read_files(
            files_path)

    def collect_month_data(self, year_month):
        month_data_records = []
        for day_data in self.weather_data_set_records:
            if self.check_valid_year_month_file(day_data.pkt, year_month):
                month_data_records.append(day_data)
        return month_data_records

    def extract_year_data(self, year):
        year_weather_record = []
        for day_data in self.weather_data_set_records:
            if self.check_valid_year_file(day_data.pkt, year):
                year_weather_record.append(day_data)
        temp_max_obj = max(year_weather_record,
                           key=lambda day_data: int(day_data.max_temperature))
        temp_min_obj = min(year_weather_record,
                           key=lambda day_data: int(day_data.min_temperature))
        max_humid_obj = max(year_weather_record,
                            key=lambda day_data: int(day_data.max_humidity))
        return temp_max_obj, temp_min_obj, max_humid_obj

    def check_valid_year_file(self, day_date, year):
        match = re.search(r'\d{4}', day_date)
        return match and (year in day_date)

    def compute_month_data_average(self, month_data_record):
        max_temp_avg = 0
        min_temp_avg = 0
        humidity_avg = 0
        count_max_temp = 0
        count_min_temp = 0
        count_humidty = 0
        for day_data in month_data_record:
            if day_data.max_temperature:
                max_temp_avg += int(day_data.max_temperature)
                count_max_temp += 1
            if day_data.min_temperature:
                min_temp_avg += int(day_data.min_temperature)
                count_min_temp += 1
            if day_data.max_humidity:
                humidity_avg += int(day_data.max_humidity)
                count_humidty += 1
        return (max_temp_avg / count_max_temp,
                min_temp_avg / count_min_temp,
                humidity_avg / count_humidty)

    def check_valid_year_month_file(self, day_date, year_month):
        match = re.search(r'\d{4}', day_date)
        if match:
            day_weather_record = day_date.split("-")
            year_and_month_record = year_month.split("/")
            return day_weather_record[0] == year_and_month_record[0] and \
                day_weather_record[1] == year_and_month_record[1]
        return False
