from result_data import ResultData


class CalculatingResults:
    def __init__(self, all_weather_readings,file_names):
        self.all_weather_readings = all_weather_readings
        self.file_names = file_names
        self.results = ResultData()

    def get_average(self, list_data):
        return round(sum(list_data) / len(list_data))

    def get_all_averages(self, month_record):
        max_temp_avg = self.get_average([int(one_record.max_temperature) for one_record in month_record
                                         if one_record.max_temperature is not ''])

        min_temp_avg = self.get_average([int(one_record.min_temperature) for one_record in month_record
                                         if one_record.min_temperature is not ''])

        mean_humidity_avg = self.get_average([int(one_record.mean_humidity) for one_record in month_record
                                              if one_record.mean_humidity is not ''])

        return max_temp_avg, min_temp_avg, mean_humidity_avg

    def calculate_results_for_year(self, year):
        year_max_temp_records = [record for file_name in self.file_names
                                 for record in self.all_weather_readings[file_name]
                                 if record.max_temperature is not '']

        year_min_temp_records = [record for file_name in self.file_names
                                 for record in self.all_weather_readings[file_name]
                                 if record.min_temperature is not '']

        year_max_humidity_records = [record for file_name in self.file_names
                                     for record in self.all_weather_readings[file_name]
                                     if record.max_humidity is not '']

        self.results.year[year] = {
            'max_temp': max(year_max_temp_records, key=lambda x: int(x.max_temperature)),
            'min_temp': min(year_min_temp_records, key=lambda x: int(x.min_temperature)),
            'max_humidity': max(year_max_humidity_records, key=lambda x: int(x.max_humidity))
        }

    def calculate_average_results_for_month(self, argument):
        for file_name in self.file_names:
            if argument in file_name:
                month_record = self.all_weather_readings[file_name]

                avg_max_temp, avg_min_temp, avg_mean_humidity = self.get_all_averages(month_record)

                self.results.month_average[argument] = {
                    'avg_max_temp': '{}C'.format(avg_max_temp),
                    'avg_min_temp': '{}C'.format(avg_min_temp),
                    'avg_mean_humidity': '{}%'.format(avg_mean_humidity)
                }

    def calculate_month_chart(self, argument):
        for file_name in self.file_names:
            if argument in file_name:
                month_record = self.all_weather_readings[file_name]

                self.results.month_chart[argument] = [record for record in month_record]
