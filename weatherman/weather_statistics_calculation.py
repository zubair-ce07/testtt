from result_data import ResultData


class WeatherStatisticsCalculation:
    def __init__(self, all_weather_readings):
        self.all_weather_readings = all_weather_readings
        self.results = ResultData()

    def get_average(self, list_data):
            return round(sum(list_data) / len(list_data)) if list_data else None

    def get_all_averages(self, month_record):
        max_temp_list = []
        min_temp_list = []
        mean_humidity_list = []

        for record in month_record:
            if record.max_temperature:
                max_temp_list.append(record.max_temperature)
            if record.min_temperature:
                min_temp_list.append(record.min_temperature)
            if record.mean_humidity:
                mean_humidity_list.append(record.mean_humidity)

        return self.get_average(max_temp_list), self.get_average(min_temp_list), self.get_average(mean_humidity_list)

    def find_max_min(self, record_list, key_expression, min_or_max):
        if not record_list:
            return
        if min_or_max == 'max':
            return max(record_list, key=key_expression)
        else:
            return min(record_list, key=key_expression)

    def get_extrema_statistics(self, year):
        year_max_temp_records = []
        year_min_temp_records = []
        year_max_humid_records = []
        all_records = self.get_records_of_argument(self.all_weather_readings, year)
        for record in all_records:
            if record.max_temperature:
                year_max_temp_records.append(record)

            if record.min_temperature:
                year_min_temp_records.append(record)

            if record.max_humidity:
                year_max_humid_records.append(record)

        self.results.year[year] = {
            'max_temp': self.find_max_min(year_max_temp_records, lambda x: x.max_temperature, 'max'),
            'min_temp': self.find_max_min(year_min_temp_records, lambda x: x.min_temperature, 'min'),
            'max_humidity': self.find_max_min(year_max_humid_records, lambda x: x.max_humidity, 'max')
        }

    def get_records_of_argument(self, all_weather_data, argument):
        return [record for date_key, record in all_weather_data.items() if argument in date_key]

    def get_average_statistics(self, argument):
        month_record = self.get_records_of_argument(self.all_weather_readings, argument)
        avg_max_temp, avg_min_temp, avg_mean_humidity = self.get_all_averages(month_record)

        self.results.month_average[argument] = {
            'avg_max_temp': avg_max_temp,
            'avg_min_temp': avg_min_temp,
            'avg_mean_humidity': avg_mean_humidity
        }

    def get_bar_chart_records(self, argument):
        self.results.month_chart[argument] = [
            record for record in self.get_records_of_argument(self.all_weather_readings, argument)
            if record.max_temperature or record.min_temperature
        ]
