from result_data import ResultData


class CalculatingResults:
    def __init__(self, all_weather_readings, file_names):
        self.all_weather_readings = all_weather_readings
        self.file_names = file_names
        self.results = ResultData()

    def get_average(self, list_data, length):
        return sum(list_data[:]) / length

    def get_years(self):
        return [file_name.split('_')[2] for file_name in self.file_names]

    def get_required_file_names(self, year):
        return [file_name for file_name in self.file_names if year in file_name]

    def calculate_results_for_year(self, year):
        self.results.year[year] = []
        max_temperature = -1000
        min_temperature = 1000
        max_humidity = -1000
        max_temp_day = ''
        min_temp_day = ''
        max_humid_day = ''
        max_temp_month = ''
        min_temp_month = ''
        max_humid_month = ''

        for file_name in self.get_required_file_names(year):
            if self.all_weather_readings.max_temperature[file_name]:
                prev_max_temp = max_temperature
                prev_min_temp = min_temperature
                prev_max_humid = max_humidity
                max_temperature = max(max_temperature, max(self.all_weather_readings.max_temperature[file_name][:]))
                min_temperature = min(min_temperature, min(self.all_weather_readings.min_temperature[file_name][:]))
                max_humidity = max(max_humidity, max(self.all_weather_readings.max_humidity[file_name][:]))

                if prev_max_temp != max_temperature:
                    max_temp_day = self.all_weather_readings.max_temperature[file_name].index(max_temperature)
                    max_temp_month = file_name.split('_')[3]

                if prev_min_temp != min_temperature:
                    min_temp_day = self.all_weather_readings.min_temperature[file_name].index(min_temperature)
                    min_temp_month = file_name.split('_')[3]

                if prev_max_humid != max_humidity:
                    max_humid_day = self.all_weather_readings.max_humidity[file_name].index(max_humidity)
                    max_humid_month = file_name.split('_')[3]

        self.results.year[year].append("{}C on {} {}".format(max_temperature, max_temp_month, max_temp_day + 1))
        self.results.year[year].append("{}C on {} {}".format(min_temperature, min_temp_month, min_temp_day + 1))
        self.results.year[year].append("{}% on {} {}".format(max_humidity, max_humid_month, max_humid_day + 1))

    def calculate_results_for_every_month(self):
        for file_name in self.file_names:
            self.results.month_average[file_name] = []
            self.results.month_chart[file_name] = []
            self.results.bonus[file_name] = []
            if self.all_weather_readings.max_temperature[file_name]:
                avg_max_temp = self.get_average(self.all_weather_readings.max_temperature[file_name],
                                                len(self.all_weather_readings.max_temperature[file_name]))

                avg_min_temp = self.get_average(self.all_weather_readings.min_temperature[file_name],
                                                len(self.all_weather_readings.min_temperature[file_name]))

                avg_mean_humidity = self.get_average(self.all_weather_readings.mean_humidity[file_name],
                                                     len(self.all_weather_readings.mean_humidity[file_name]))

                self.results.month_average[file_name].append("{}C".format(avg_max_temp))
                self.results.month_average[file_name].append("{}C".format(avg_min_temp))
                self.results.month_average[file_name].append("{}%".format(avg_mean_humidity))

                max_temp_list = self.all_weather_readings.max_temperature[file_name]
                min_temp_list = self.all_weather_readings.min_temperature[file_name]

                self.results.bonus[file_name].append("\nBonus Task\n")

                for index, value in enumerate(max_temp_list):
                    self.results.month_chart[file_name].append("{}{} {} {}{}".format('\033[91m', index + 1, '+' * value, value, 'C'))
                    self.results.month_chart[file_name].append("{}{} {} {}{}".format('\033[94m', index + 1,
                                                               '+' * min_temp_list[index], min_temp_list[index], 'C'))

                    self.results.bonus[file_name].append(
                        "{} {}{}{}{} {}{}-{}{}".format(index + 1, '\033[94m', '+' * min_temp_list[index],
                                                       '\033[91m', '+' * value, min_temp_list[index],
                                                       'C', value, 'C'))

    def calculations(self):
        years = self.get_years()
        for year in years:
            self.calculate_results_for_year(year)

        self.calculate_results_for_every_month()

