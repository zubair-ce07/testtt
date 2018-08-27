class YearWeather:

    def __init__(self):
        self.year_weather = {}

    def highest_temperature_day(self):
        pass

    def add_year_weather(self, mw, year):
        kls = list(mw.month_weather.keys())
        if year in self.year_weather:
            self.year_weather[year][kls[0]] = mw
        else:
            self.year_weather[year] = {}
            self.year_weather[year][kls[0]] = mw

    def highest_temperature_day(self, year):
        if year in self.year_weather:
            temp_data = [-99, -1]
            mws = self.year_weather[year]
            for mw in mws:
                t_d = mws[mw].highest_temperature_day(mw)
                if t_d[0] > temp_data[0]:
                    temp_data = t_d

            return temp_data

        else:
            return "This Year Does'nt Exist in our database"

    def lowest_temperature_day(self, year):
        if year in self.year_weather:
            temp_data = [99, -1]
            mws = self.year_weather[year]
            for mw in mws:
                t_d = mws[mw].lowest_temperature_day(mw)
                if t_d[0] < temp_data[0]:
                    temp_data = t_d

            return temp_data

        else:
            return "This Year Does'nt Exist in our database"

    def max_humidity(self, year):
        if year in self.year_weather:
            humidity = [-99, -1]
            mws = self.year_weather[year]
            for mw in mws:
                t_d = mws[mw].max_humidity(mw)
                if t_d[0] > humidity[0]:
                    humidity = t_d
            return humidity

        else:
            return "This Year Does'nt Exist in our database"

    def average_highest_temperature(self, year, month):
        if year in self.year_weather:
            mws = self.year_weather[year]
            if month in mws:
                mw = mws[month]
                return mw.average_highest_temperature(month)
            else:
                return "This Month does'nt exist"
        else:
            return "This Year Does'nt Exist in our database"

    def average_lowest_temperature(self, year, month):
        if year in self.year_weather:
            mws = self.year_weather[year]
            if month in mws:
                mw = mws[month]
                return mw.average_lowest_temperature(month)
            else:
                return "This Month does'nt exist"
        else:
            return "This Year Does'nt Exist in our database"

    def average_mean_humidity(self, year, month):
        if year in self.year_weather:
            mws = self.year_weather[year]
            if month in mws:
                mw = mws[month]
                return mw.average_mean_humidity(month)
            else:
                return "This Month does'nt exist"
        else:
            return "This Year Does'nt Exist in our database"

    def print_bar_chart(self, year, month):
        if year in self.year_weather:
            mws = self.year_weather[year]
            if month in mws:
                mw = mws[month]
                return mw.print_bar_chart(month)
            else:
                return "This Month does'nt exist"
        else:
            return "This Year Does'nt Exist in our database"

    def print_bar_chart2(self, year, month):
        if year in self.year_weather:
            mws = self.year_weather[year]
            if month in mws:
                mw = mws[month]
                return mw.print_bar_chart2(month)
            else:
                return "This Month does'nt exist"
        else:
            return "This Year Does'nt Exist in our database"
