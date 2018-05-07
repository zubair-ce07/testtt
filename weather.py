import os.path
from weatherReport import *
from weatherData import *

class Weather:

    def __init__(self):
        self.weather_data = weatherData();

    def read_data_for_month(self, filepath):
        total_days_count = 0
        self.month_file = filepath
        highest_average = 0
        lowest_average = 0
        average_mean_humidity = 0
        max_temperature = []
        min_temperature = []

        with open(self.month_file) as weather_details:

            next(weather_details)
            for line in weather_details:
                weather_parameters = line.split(',')

                for weather_parameters_index,weather_parameter in enumerate (weather_parameters):
                    if weather_parameters[weather_parameters_index] == '':
                        weather_parameters[weather_parameters_index] = '0'

                max_temperature.append(int(weather_parameters[1]))
                min_temperature.append(int(weather_parameters[3]))

                highest_average += int(weather_parameters[1])
                lowest_average += int(weather_parameters[3])
                average_mean_humidity += int(weather_parameters[8])
                total_days_count += 1


            highest_average = int(highest_average / total_days_count)
            lowest_average = int(lowest_average / total_days_count)
            average_mean_humidity = int(average_mean_humidity / total_days_count)
        weather_details.close()
        self.weather_data.initialize_monthly_data(highest_average,lowest_average,average_mean_humidity,max_temperature,min_temperature)

    def read_files_for_particular_year(self,filenames):
        self.years_filenames = filenames

        highest_temperature = -100
        lowest_temperature = 100
        highest_humidity = -100
        hightest_temperature_date = ''
        lowest_temperature_date = ''
        highest_humidity_date = ''

        for month_wise_files_counter in self.years_filenames:
            if os.path.exists(month_wise_files_counter):
                with open(month_wise_files_counter) as weather_details:
                    next(weather_details)
                    for line in weather_details:
                        weather_parameters = line.split(',')

                        if weather_parameters[1] is not '':
                            if int(weather_parameters[1]) > highest_temperature:
                                highest_temperature = int(weather_parameters[1])
                                hightest_temperature_date = weather_parameters[0]

                        if weather_parameters[3] is not '':
                            if int(weather_parameters[3]) < lowest_temperature:
                                lowest_temperature = int(weather_parameters[3])
                                lowest_temperature_date = weather_parameters[0]

                        if weather_parameters[7] is not '':
                            if int(weather_parameters[7]) > highest_humidity:
                                highest_humidity = int(weather_parameters[7])
                                highest_humidity_date = weather_parameters[0]

                weather_details.close()
        self.weather_data.initialize_yearly_data(highest_temperature,lowest_temperature,highest_humidity,hightest_temperature_date,lowest_temperature_date,highest_humidity_date)


class YearlyWeather(Weather):

    def __init__(self,filenames):
        Weather.__init__(self)
        self.filenames = filenames
        self.read_files_for_particular_year (self.filenames)

    def verify_yearly_data(self):
        file_found = False
        for file_count in self.filenames:
            if os.path.exists(file_count):
                return True

        return False

    def get_yearly_weather(self):
        return self.weather_data.get_yearly_weather_details()


class MonthlyWeather(Weather):

    def __init__(self,filepath):
        Weather.__init__(self)
        self.filepath = filepath
        return self.read_data_for_month(self.filepath)

    def verify_monthly_data(self):
        file_found = False

        if os.path.exists(self.filepath):
            file_found = True

        return file_found

    def get_monthly_weather(self):
        return self.weather_data.get_monthly_weather_details()

    def get_daily_temperature(self):
        monthly_max_readings = self.weather_data.get_monthly_max_readings()
        monthly_min_readings = self.weather_data.get_monthly_min_readings()

        for index,value in enumerate (monthly_max_readings):
            weather_graph = WeatherReport(monthly_max_readings[index],monthly_min_readings[index])
            print('\033[91m'+str(index+1),end='')
            weather_graph.max_temperature_graph(str(index+1))
            print ('\033[91m'+'('+str(monthly_max_readings[index])+')')
            print('\033[94m'+str(index+1),end='')
            weather_graph.min_temperature_graph(str(index+1))
            print ('\033[94m'+'('+str(monthly_min_readings[index])+')')

    def read_data_for_daily_graph(self):
        monthly_max_readings = self.weather_data.get_monthly_max_readings()
        monthly_min_readings = self.weather_data.get_monthly_min_readings()

        for index,value in enumerate (monthly_max_readings):
            weather_graph = WeatherReport(monthly_max_readings[index],monthly_min_readings[index])
            weather_graph.merged_graph(str(index+1))
