import csv

from weatherman.weather import Weather


class WeatherReport:
    months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep",
              10: "Oct", 11: "Nov", 12: "Dec"}

    months_complete_name = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April", "May": "May",
                            "Jun": "June", "Jul": "July", "Aug": "August", "Sep": "September", "Oct": "October",
                            "Nov": "November", "Dec": "December"}

    weather_keys = {1: 'PKT', 2: 'Max TemperatureC', 3: 'Mean TemperatureC', 4: 'Min TemperatureC',
                    5: 'Dew PointC', 6: 'MeanDew PointC', 7: 'Min DewpointC', 8: 'Max Humidity',
                    9: ' Mean Humidity', 10: ' Min Humidity', 11: ' Max Sea Level PressurehPa',
                    12: ' Mean Sea Level PressurehPa',
                    13: ' Min Sea Level PressurehPa', 14: ' Max VisibilityKm', 15: ' Mean VisibilityKm',
                    16: ' Min VisibilitykM',
                    17: ' Max Wind SpeedKm/h', 18: ' Mean Wind SpeedKm/h', 19: ' Max Gust SpeedKm/h',
                    20: 'Precipitationmm',
                    21: ' CloudCover', 22: ' Events', 23: 'WindDirDegrees'}

    def __read_month_weather(self, file_path):
        month_data = []
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                month_data.append(row)
        return month_data

    def sort_on_max_temp(self, a):
        return int(a.weather[self.weather_keys[2]])

    def sort_on_max_humid(self, a):
        return int(a.weather[self.weather_keys[8]])

    def sort_on_min_temp(self, a):
        return int(a.weather[self.weather_keys[4]])

    def __get_month_name(self, month_number):
        return self.months_complete_name[self.months[int(month_number)]]

    def __get_day_weather(self, day_data):
        day_weather = Weather()
        day_weather.set_weather(day_data)
        return day_weather

    def get_max_value(self, data, option):
        if option == 1:
            data = sorted(data, key=self.sort_on_max_temp, reverse=True)
        if option == 2:
            data = sorted(data, key=self.sort_on_max_humid, reverse=True)
        return data[0]

    def get_min_value(self, data, option):
        if option == 1:
            data = sorted(data, key=self.sort_on_min_temp)
        return data[0]

    def print_info(self, day_weather, option, msg):
        print(msg + ': ' + day_weather.weather[self.weather_keys[option]] + 'c on ' + self.__get_month_name(
            day_weather.weather['PKT'].split('-')[1]) +
              ' ' + day_weather.weather['PKT'].split('-')[2])

    def get_yearly_insights(self, year, files_path):
        year_data = []
        file = open('files_names', 'rU')
        files_names = file.read().split('\n')[:-1]
        file.close()
        for file_name in files_names:
            if year == file_name.split('_')[2]:
                month_data = self.__read_month_weather(files_path + '/' + file_name)
                for data in month_data:
                    year_data.append(self.__get_day_weather(data))
        max_temperature_day = self.get_max_value(year_data, 1)
        self.print_info(max_temperature_day, 2, "Highest")
        min_temperature_day = self.get_min_value(year_data, 1)
        self.print_info(min_temperature_day, 4, "Lowest")
        max_humidity_day = self.get_max_value(year_data, 2)
        self.print_info(max_humidity_day, 8, "Humidity")
        return None
