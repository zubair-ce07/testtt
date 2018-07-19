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
                max_temp_list.append(int(record.max_temperature))
            if record.min_temperature:
                min_temp_list.append(int(record.min_temperature))
            if record.mean_humidity:
                mean_humidity_list.append(int(record.mean_humidity))

        max_temp_avg = self.get_average(max_temp_list)
        min_temp_avg = self.get_average(min_temp_list)
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

        self.results.year[year] = {
            'max_temp': max(year_max_temp_records, key=lambda x: int(x.max_temperature)),
            'min_temp': min(year_min_temp_records, key=lambda x: int(x.min_temperature)),
            'max_humidity': max(year_max_humid_records, key=lambda x: int(x.max_humidity))
        }

    def get_month_record(self, all_weather_data, argument):
        return [record for date_key, record in all_weather_data.items() if argument in date_key]

    def calculate_average_results_for_month(self, argument):
        month_record = self.get_month_record(self.all_weather_readings, argument)
        avg_max_temp, avg_min_temp, avg_mean_humidity = self.get_all_averages(month_record)

        self.results.month_average[argument] = {
            'avg_max_temp': '{}C'.format(avg_max_temp),
            'avg_min_temp': '{}C'.format(avg_min_temp),
            'avg_mean_humidity': '{}%'.format(avg_mean_humidity)
        }

    def calculate_month_chart(self, argument):
        self.results.month_chart[argument] = self.get_month_record(self.all_weather_readings, argument)
