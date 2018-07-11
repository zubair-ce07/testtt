from result_data import ResultData


class CalculatingResults:
    def __init__(self, all_weather_readings, file_names, flag):
        self.all_weather_readings = all_weather_readings
        self.file_names = file_names
        self.flag = flag

    def calculations(self):
        if self.flag == '-e':
            max_temperature = -1000
            min_temperature = 1000
            max_humidity = -1000
            max_temp_day = ''
            min_temp_day = ''
            max_humid_day = ''
            max_temp_month = ''
            min_temp_month = ''
            max_humid_month = ''

            for file_name in self.file_names:
                file_name  = file_name.replace('.txt', '')
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

            results = ResultData()
            results.year.append("{}C on {} {}".format(max_temperature, max_temp_month, max_temp_day+1))
            results.year.append("{}C on {} {}".format(min_temperature, min_temp_month, min_temp_day+1))
            results.year.append("{}% on {} {}".format(max_humidity, max_humid_month, max_humid_day+1))

            return results
        elif self.flag == '-a':
            file_name = self.file_names[0].replace('.txt', '')
            if self.all_weather_readings.max_temperature[file_name]:
                max_temp_sum = sum(self.all_weather_readings.max_temperature[file_name][:])
                avg_max_temp = max_temp_sum / len(self.all_weather_readings.max_temperature[file_name])

                min_temp_sum = sum(self.all_weather_readings.min_temperature[file_name][:])
                avg_min_temp = min_temp_sum / len(self.all_weather_readings.min_temperature[file_name])

                mean_humidity_sum = sum(self.all_weather_readings.mean_humidity[file_name][:])
                avg_mean_humidity = mean_humidity_sum / len(self.all_weather_readings.mean_humidity[file_name])

                results = ResultData()
                results.month.append("{}C".format(avg_max_temp))
                results.month.append("{}C".format(avg_min_temp))
                results.month.append("{}%".format(avg_mean_humidity))
                return results
        else:
            file_name = self.file_names[0].replace('.txt', '')
            if self.all_weather_readings.max_temperature[file_name]:
                max_temp_list = self.all_weather_readings.max_temperature[file_name]
                min_temp_list = self.all_weather_readings.min_temperature[file_name]
                results = ResultData()

                results.month.append("{} {}".format(file_name.split('_')[3], file_name.split('_')[2]))
                results.month.append('\n')

                results.bonus.append("\nBonus Task\n")

                for index, value in enumerate(max_temp_list):
                    results.month.append("{}{} {} {}{}".format('\033[91m', index+1, '+'*value, value, 'C'))
                    results.month.append("{}{} {} {}{}".format('\033[94m', index+1,
                                                               '+'*min_temp_list[index], min_temp_list[index], 'C'))

                    results.bonus.append("{} {}{}{}{} {}{}-{}{}".format(index+1, '\033[94m', '+'*min_temp_list[index],
                                                                        '\033[91m',  '+' * value, min_temp_list[index],
                                                                        'C', value, 'C'))

                return results




