from result_data import ResultData


class CalculatingResults:
    def __init__(self, all_weather_readings):
        self.all_weather_readings = all_weather_readings
        self.results = ResultData()

    def get_average(self, list_data):
        return round(sum(list_data) / len(list_data))

    def get_all_averages(self, month_record):
        max_temp_avg = self.get_average([int(record.max_temperature) for record in month_record
                                         if record.max_temperature is not ''])

        min_temp_avg = self.get_average([int(record.min_temperature) for record in month_record
                                         if record.min_temperature is not ''])

        mean_humidity_avg = self.get_average([int(record.mean_humidity) for record in month_record
                                              if record.mean_humidity is not ''])

        return max_temp_avg, min_temp_avg, mean_humidity_avg

    def calculate_results_for_year(self, year):
        year_max_temp_records = [self.all_weather_readings[date_key] for date_key in self.all_weather_readings.keys()
                                 if year in date_key
                                 and self.all_weather_readings[date_key].max_temperature is not '']

        year_min_temp_records = [self.all_weather_readings[date_key] for date_key in self.all_weather_readings.keys()
                                 if year in date_key
                                 and self.all_weather_readings[date_key].min_temperature is not '']

        year_max_humid_records = [self.all_weather_readings[date_key] for date_key in self.all_weather_readings.keys()
                                  if year in date_key
                                  and self.all_weather_readings[date_key].max_humidity is not '']

        self.results.year[year] = {
            'max_temp': max(year_max_temp_records, key=lambda x: int(x.max_temperature)),
            'min_temp': min(year_min_temp_records, key=lambda x: int(x.min_temperature)),
            'max_humidity': max(year_max_humid_records, key=lambda x: int(x.max_humidity))
        }

    def calculate_average_results_for_month(self, argument):
        month_record = [self.all_weather_readings[date_key] for date_key in self.all_weather_readings.keys()
                        if argument in date_key]

        avg_max_temp, avg_min_temp, avg_mean_humidity = self.get_all_averages(month_record)

        self.results.month_average[argument] = {
            'avg_max_temp': '{}C'.format(avg_max_temp),
            'avg_min_temp': '{}C'.format(avg_min_temp),
            'avg_mean_humidity': '{}%'.format(avg_mean_humidity)
        }

    def calculate_month_chart(self, argument):
            month_record = [self.all_weather_readings[date_key] for date_key in self.all_weather_readings.keys()
                            if argument in date_key]

            self.results.month_chart[argument] = [record for record in month_record]
