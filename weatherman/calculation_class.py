from result_data import ResultData


class CalculatingResults:
    def __init__(self, all_weather_readings, argument_list, file_names):
        self.all_weather_readings = all_weather_readings
        self.argument_list = argument_list
        self.file_names = file_names
        self.results = ResultData()

    def get_average(self, list_data):
        return sum(list_data) / len(list_data)

    def get_all_averages(self, month_record):
        max_temp_avg = self.get_average([int(one_record.max_temperature) for one_record in month_record
                                         if one_record.max_temperature is not ''])

        min_temp_avg = self.get_average([int(one_record.min_temperature) for one_record in month_record
                                         if one_record.min_temperature is not ''])

        mean_humidity_avg = self.get_average([int(one_record.mean_humidity) for one_record in month_record
                                              if one_record.mean_humidity is not ''])

        return max_temp_avg, min_temp_avg, mean_humidity_avg

    def calculate_results_for_year(self, year):
        self.results.year[year] = []

        one_year_max_temp_records = [(one_record.pkt, int(one_record.max_temperature))
                                     for file_name in self.file_names
                                     for one_record in self.all_weather_readings[file_name]
                                     if one_record.max_temperature is not '']

        one_year_min_temp_records = [(one_record.pkt, int(one_record.min_temperature))
                                     for file_name in self.file_names
                                     for one_record in self.all_weather_readings[file_name]
                                     if one_record.min_temperature is not '']

        one_year_max_humidity_records = [(one_record.pkt, int(one_record.max_humidity))
                                         for file_name in self.file_names
                                         for one_record in self.all_weather_readings[file_name]
                                         if one_record.max_humidity is not '']

        self.results.year[year].append(max(one_year_max_temp_records, key=lambda x: x[1]))
        self.results.year[year].append(min(one_year_min_temp_records, key=lambda x: x[1]))
        self.results.year[year].append(max(one_year_max_humidity_records, key=lambda x: x[1]))

    def calculate_average_results_for_month(self, argument):
        for file_name in self.file_names:
            if argument in file_name:
                self.results.month_average[argument] = []

                month_record = self.all_weather_readings[file_name]

                avg_max_temp, avg_min_temp, avg_mean_humidity = self.get_all_averages(month_record)

                self.results.month_average[argument].append("{}C".format(avg_max_temp))
                self.results.month_average[argument].append("{}C".format(avg_min_temp))
                self.results.month_average[argument].append("{}%".format(avg_mean_humidity))

                self.results.month_chart[argument] = [[one_record.pkt.day, one_record.max_temperature,
                                                       one_record.min_temperature] for one_record in month_record]

    def calculations(self):
        for argument in self.argument_list:
            if str.isnumeric(argument):
                self.calculate_results_for_year(argument)
            else:
                self.calculate_average_results_for_month(argument)


