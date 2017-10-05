import csv

from weatherman.weather import Weather


class WeatherReport:
    files_names = []

    months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep",
              10: "Oct", 11: "Nov", 12: "Dec"}

    months_complete_name = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April", "May": "May",
                            "Jun": "June", "Jul": "July", "Aug": "August", "Sep": "September", "Oct": "October",
                            "Nov": "November", "Dec": "December"}

    WEATHER_KEY_MAP = {1: 'PKT', 2: 'Max TemperatureC', 3: 'Mean TemperatureC', 4: 'Min TemperatureC',
                       5: 'Dew PointC', 6: 'MeanDew PointC', 7: 'Min DewpointC', 8: 'Max Humidity',
                       9: ' Mean Humidity', 10: ' Min Humidity', 11: ' Max Sea Level PressurehPa',
                       12: ' Mean Sea Level PressurehPa',
                       13: ' Min Sea Level PressurehPa', 14: ' Max VisibilityKm', 15: ' Mean VisibilityKm',
                       16: ' Min VisibilitykM',
                       17: ' Max Wind SpeedKm/h', 18: ' Mean Wind SpeedKm/h', 19: ' Max Gust SpeedKm/h',
                       20: 'Precipitationmm',
                       21: ' CloudCover', 22: ' Events', 23: 'WindDirDegrees'}

    def __init__(self):
        file = open('files_names', 'rU')
        self.files_names = file.read().split('\n')[:-1]
        file.close()

    def __read_month_weather(self, file_path):
        month_data = []
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                month_data.append(row)
        return month_data

    def __get_month_name(self, month_number):
        return self.months_complete_name[self.months[int(month_number)]]

    def __get_day_weather(self, day_data):
        day_weather = Weather()
        day_weather.set_weather(day_data)
        return day_weather

    def __compute_average(self, data):
        average_max_temperature = sum(int(line.weather['Max TemperatureC']) for line in data)/len(data)
        average_min_temperature = sum(int(line.weather['Min TemperatureC']) for line in data)/len(data)
        average_mean_humidity = sum(int(line.weather['Mean Humidity']) for line in data)/len(data)
        print(average_mean_humidity)
        return None

    def get_required_day(self, data, option):
        if option == 1:
            return max(data, key=lambda x: int(x.weather['Max TemperatureC']))
        if option == 2:
            return min(data, key=lambda x: int(x.weather['Min TemperatureC']))
        if option == 3:
            return max(data, key=lambda x: int(x.weather['Max Humidity']))
        return data[0]

    def print_yearly_report(self,highest_temp_day, lowest_temp_day, highest_humidity_day):
        print('Highest: ' + highest_temp_day.weather['Max TemperatureC'] + 'c on '
              + self.__get_month_name(highest_temp_day.weather['PKT'].split('-')[1])
              + ' ' + highest_temp_day.weather['PKT'].split('-')[2])

        print('Highest: ' + lowest_temp_day.weather['Min TemperatureC'] + 'c on '
              + self.__get_month_name(lowest_temp_day.weather['PKT'].split('-')[1])
              + ' ' + lowest_temp_day.weather['PKT'].split('-')[2])

        print('Highest: ' + highest_humidity_day.weather['Max Humidity'] + '% on '
              + self.__get_month_name(highest_humidity_day.weather['PKT'].split('-')[1])
              + ' ' + highest_humidity_day.weather['PKT'].split('-')[2])

    def get_month_data(self, year_and_month, files_path):
        month_data = []
        year = year_and_month.split('/')[0]
        month = year_and_month.split('/')[1]
        months_key = {v: k for k, v in self.months.items()}
        for file_name in self.files_names:
            if year == file_name.split('_')[2] and month == str(months_key[file_name.split('_')[3].split('.')[0]]):
                file_data = self.__read_month_weather(files_path + '/' + file_name)
                for data in file_data:
                    if data['Max TemperatureC'] and data['Min TemperatureC'] and data['Max Humidity']:
                        month_data.append(self.__get_day_weather(data))
        month_name = self.months_complete_name[self.months[int(month)]]
        return month_name, month_data

    def print_dayily_data(self, month_name, month_data):
        return None

    def get_yearly_insights(self, year, files_path):
        year_data = []
        for file_name in self.files_names:
            if year == file_name.split('_')[2]:
                month_data = self.__read_month_weather(files_path + '/' + file_name)
                for data in month_data:
                    if data['Max TemperatureC'] and data['Min TemperatureC']and data['Max Humidity']:
                        year_data.append(self.__get_day_weather(data))
        highest_temperature_day = self.get_required_day(year_data, 1)
        lowest_temperature_day = self.get_required_day(year_data, 2)
        highest_humidity_day = self.get_required_day(year_data, 3)
        self.print_yearly_report(highest_temperature_day, lowest_temperature_day, highest_humidity_day)
        return None

    def get_monthly_insights(self, year_and_month, files_path):
        month_name, month_data = self.get_month_data(year_and_month, files_path)
        self.__compute_average(month_data)

    def get_days_insights(self, year_and_month, files_path):
        month_name, month_data = self.get_month_data(year_and_month, files_path)
        self.print_dayily_data(month_name, month_data)
        return None
