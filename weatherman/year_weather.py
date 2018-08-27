class YearWeather:

    def __init__(self):
        self.year_weather = {}

    def highest_temperature_day(self):
        pass

    def add_year_weather(self, month_weather, year):
        keys_list = list(month_weather.month_weather.keys())
        if year in self.year_weather:
            self.year_weather[year][keys_list[0]] = month_weather
        else:
            self.year_weather[year] = {}
            self.year_weather[year][keys_list[0]] = month_weather

    def highest_temperature_day(self, year):
        if year in self.year_weather:
            high_temp = [-99, -1]
            monthly_weathers = self.year_weather[year]
            for monthly_weather in monthly_weathers:
                temp_data = monthly_weathers[monthly_weather].highest_temperature_day(monthly_weather)
                if temp_data[0] > high_temp[0]:
                    high_temp = temp_data

            return high_temp

        else:
            return "This Year Does'nt Exist in our database"

    def lowest_temperature_day(self, year):
        if year in self.year_weather:
            low_temp = [99, -1]
            monthly_weathers = self.year_weather[year]
            for monthly_weather in monthly_weathers:
                temp_data = monthly_weathers[monthly_weather].lowest_temperature_day(monthly_weather)
                if temp_data[0] < low_temp[0]:
                    low_temp = temp_data

            return low_temp

        else:
            return "This Year Does'nt Exist in our database"

    def max_humidity(self, year):
        if year in self.year_weather:
            humidity = [-99, -1]
            monthly_weathers = self.year_weather[year]
            for monthly_weather in monthly_weathers:
                temp_data = monthly_weathers[monthly_weather].max_humidity(monthly_weather)
                if temp_data[0] > humidity[0]:
                    humidity = temp_data
            return humidity

        else:
            return "This Year Does'nt Exist in our database"

    def average_highest_temperature(self, year, month):
        if year in self.year_weather:
            monthly_weathers = self.year_weather[year]
            if month in monthly_weathers:
                monthly_weather = monthly_weathers[month]
                return monthly_weather.average_highest_temperature(month)
            else:
                return "This Month does'nt exist"
        else:
            return "This Year Does'nt Exist in our database"

    def average_lowest_temperature(self, year, month):
        if year in self.year_weather:
            monthly_weathers = self.year_weather[year]
            if month in monthly_weathers:
                monthly_weather = monthly_weathers[month]
                return monthly_weather.average_lowest_temperature(month)
            else:
                return "This Month does'nt exist"
        else:
            return "This Year Does'nt Exist in our database"

    def average_mean_humidity(self, year, month):
        if year in self.year_weather:
            monthly_weathers = self.year_weather[year]
            if month in monthly_weathers:
                monthly_weather = monthly_weathers[month]
                return monthly_weather.average_mean_humidity(month)
            else:
                return "This Month does'nt exist"
        else:
            return "This Year Does'nt Exist in our database"

    def print_bar_chart(self, year, month):
        if year in self.year_weather:
            monthly_weathers = self.year_weather[year]
            if month in monthly_weathers:
                monthly_weather = monthly_weathers[month]
                return monthly_weather.print_bar_chart(month)
            else:
                return "This Month does'nt exist"
        else:
            return "This Year Does'nt Exist in our database"

    def print_bar_chart2(self, year, month):
        if year in self.year_weather:
            monthly_weathers = self.year_weather[year]
            if month in monthly_weathers:
                monthly_weather = monthly_weathers[month]
                return monthly_weather.print_bar_chart2(month)
            else:
                return "This Month does'nt exist"
        else:
            return "This Year Does'nt Exist in our database"
