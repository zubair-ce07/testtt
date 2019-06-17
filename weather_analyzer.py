from weather_data_parser import WeatherDataParser


class WeatherAnalyzer:
    def __init__(self):
        self.weather_data_set_records = []

    def collect_weather_data_set(self, files_path):
        weather_data_parser = WeatherDataParser()
        self.weather_data_set_records = weather_data_parser.parse(
            files_path)

    def collect_month_data(self, year_month):
        month_data_records = []
        for day_weather_record in self.weather_data_set_records:
            if self.check_valid_year_month_file(day_weather_record.pkt,
                                                year_month):
                month_data_records.append(day_weather_record)
        return month_data_records

    def extract_year_data(self, year):
        year_weather_record = []
        for day_record in self.weather_data_set_records:
            if self.check_valid_year_file(day_record.pkt, year):
                year_weather_record.append(day_record)
        temp_max_obj = max(year_weather_record,
                           key=lambda day_data: int(day_data.max_temperature))
        temp_min_obj = min(year_weather_record,
                           key=lambda day_data: int(day_data.min_temperature))
        max_humid_obj = max(year_weather_record,
                            key=lambda day_data: int(day_data.max_humidity))
        return temp_max_obj, temp_min_obj, max_humid_obj

    def check_valid_year_file(self, day_date, year):
        return int(year) == day_date.year

    def compute_month_data_average(self, month_data_record):
        mean_humidity_avg = sum(int(day_record.mean_humidity) for day_record in
                                month_data_record) / len(month_data_record)
        min_temp_avg = sum(int(day_record.min_temperature) for day_record in
                           month_data_record) / len(month_data_record)
        max_temp_avg = sum(int(day_record.max_temperature) for day_record in
                           month_data_record) / len(month_data_record)
        return max_temp_avg, min_temp_avg, mean_humidity_avg

    def check_valid_year_month_file(self, day_date, year_month):
        year_and_month_record = year_month.split("/")
        return day_date.year == int(year_and_month_record[0]) and \
            day_date.month == int(year_and_month_record[1])
