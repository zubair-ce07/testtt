
class MonthWeather:

    def __init__(self):
        self.month_weather = {}

    def add_month_weather(self, daily_weather, month):
        self.month_weather[month] = daily_weather

    def highest_temperature_day(self, month):
        if month in self.month_weather:
            return self.month_weather[month].highest_temperature_day()
        else:
            return "We don't Have data of this year's Month"

    def lowest_temperature_day(self, month):
        if month in self.month_weather:
            return self.month_weather[month].lowest_temperature_day()
        else:
            return "We don't Have data of this year's Month"

    def max_humidity(self, month):
        if month in self.month_weather:
            return self.month_weather[month].max_humidity()
        else:
            return "We don't Have data of this year's Month"

    def average_highest_temperature(self, month):
        return self.month_weather[month].average_highest_temperature()

    def average_lowest_temperature(self, month):
        return self.month_weather[month].average_lowest_temperature()

    def average_mean_humidity(self, month):
        return self.month_weather[month].average_mean_humidity()

    def print_bar_chart(self, month):
        daily_weather = self.month_weather[month]
        counter = 1
        print(daily_weather.day_weather[counter].pkt_dt.strftime("%b %Y"))
        while counter <= len(daily_weather.day_weather):

            if daily_weather.day_weather[counter].tempC[0] is not None:
                print('\x1b[3;31m' + str(counter) + " " + str(abs(int(daily_weather.day_weather[counter].tempC[0]))*'+') + ' ' + daily_weather.day_weather[counter].tempC[0] + "C" + '\x1b[0m')
                print('\x1b[3;34m' + str(counter) + " " + str(abs(int(daily_weather.day_weather[counter].tempC[2]))*'+') + ' ' + daily_weather.day_weather[counter].tempC[2] + "C" + '\x1b[0m')

            counter += 1

    def print_bar_chart2(self, month):
        daily_weather = self.month_weather[month]
        counter = 1
        print(daily_weather.day_weather[counter].pkt_dt.strftime("%b %Y"))
        while counter <= len(daily_weather.day_weather):

            if daily_weather.day_weather[counter].tempC[0] is not None:
                print('\x1b[3;34m' + str(counter) + " " + str(abs((int(daily_weather.day_weather[counter].tempC[2]))) * '+') + '\x1b[3;31m' + str(abs((int(daily_weather.day_weather[counter].tempC[0]))) * '+') + ' ' +
                      daily_weather.day_weather[counter].tempC[2] + "C" + " - " + daily_weather.day_weather[counter].tempC[0] + "C" + '\x1b[0m')

            counter += 1
