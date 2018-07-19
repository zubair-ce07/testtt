from result_data import ResultData


class CalculatingResults:
    def __init__(self, all_weather_readings):
        self.all_weather_readings = all_weather_readings
        self.results = ResultData()

    def get_average(self, list_data):
        return round(sum(list_data) / len(list_data))

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

        max_temp_avg = None
        mean_humidity_avg = None
        min_temp_avg = None

        if max_temp_list:
            max_temp_avg = self.get_average(max_temp_list)
        if min_temp_list:
            min_temp_avg = self.get_average(min_temp_list)
        if mean_humidity_list:
            mean_humidity_avg = self.get_average(mean_humidity_list)

        return max_temp_avg, min_temp_avg, mean_humidity_avg

    def calculate_results_for_year(self, year):
        year_max_temp_records = []
        year_min_temp_records = []
        year_max_humid_records = []

        for date_key, record in self.all_weather_readings.items():
            if year in date_key:
                if record.max_temperature:
                    year_max_temp_records.append(record)

                if record.min_temperature:
                    year_min_temp_records.append(record)

                if record.max_humidity:
                    year_max_humid_records.append(record)
        max_temp = None
        min_temp = None
        max_humidity = None
        if year_max_temp_records:
            max_temp = max(year_max_temp_records, key=lambda x: x.max_temperature)
        if year_min_temp_records:
            min_temp = min(year_min_temp_records, key=lambda x: x.min_temperature)
        if year_max_humid_records:
            max_humidity = max(year_max_humid_records, key=lambda x: x.max_humidity)

        self.results.year[year] = {
            'max_temp': max_temp,
            'min_temp': min_temp,
            'max_humidity': max_humidity
        }

    def get_month_record(self, all_weather_data, argument):
        return [record for date_key, record in all_weather_data.items() if argument in date_key]

    def calculate_average_results_for_month(self, argument):
        month_record = self.get_month_record(self.all_weather_readings, argument)
        avg_max_temp, avg_min_temp, avg_mean_humidity = self.get_all_averages(month_record)

        self.results.month_average[argument] = {
            'avg_max_temp': avg_max_temp,
            'avg_min_temp': avg_min_temp,
            'avg_mean_humidity': avg_mean_humidity
        }

    def calculate_month_chart(self, argument):
        self.results.month_chart[argument] = self.get_month_record(self.all_weather_readings, argument)
