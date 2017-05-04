from dailyweathermodel import DailyWeatherModel
import csv


class MonthWeatherModel:
    def __init__(self, file_name):  # this class reads data from one file
        self.day_weather_info_array = []
        file_path = "weatherfiles/" + file_name
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                current_day_weather = DailyWeatherModel(row)
                self.day_weather_info_array.append(current_day_weather)

    def print_highest_lowest_chart(self):
        for current_day_weather in self.day_weather_info_array:
            current_day_weather.print_chart_string()

    def find_max_for_attribute(self, attribute):
        max_model = self.day_weather_info_array[0]
        max_val = self.day_weather_info_array[0].__getattribute__(attribute)
        for day_model in self.day_weather_info_array:
            cur_val = day_model.__getattribute__(attribute)
            try:
                if int(cur_val) > int(max_val):
                    max_val = cur_val
                    max_model = day_model
            except:
                continue
        return max_model

    def find_min_for_attribute(self, attribute):
        min_model = self.day_weather_info_array[0]
        min_val = self.day_weather_info_array[0].__getattribute__(attribute)
        for day_model in self.day_weather_info_array:
            cur_val = day_model.__getattribute__(attribute)
            try:
                if int(cur_val) < int(min_val):
                    min_val = cur_val
                    min_model = day_model
            except:
                continue
        return min_model

    def find_average_for_attribute(self, attribute):
        sum_of_all_values = 0.0
        for day_model in self.day_weather_info_array:
            cur_val = day_model.__getattribute__(attribute)
            try:
                if float(cur_val):
                    sum_of_all_values = sum_of_all_values + float(cur_val)
            except:
                continue
        return sum_of_all_values/(len(self.day_weather_info_array))
