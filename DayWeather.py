class DayWeather:

    def __init__(self):
        self.day_weather = {}

    def add_weather(self, weather, day):
        self.day_weather[day] = weather

    def highest_temperature_day(self):
        temp_date = [-99, -1]
        for day in self.day_weather:
            if self.day_weather[day].tempC[0] is not None:
                if int(self.day_weather[day].tempC[0]) > temp_date[0]:
                    temp_date = int(self.day_weather[day].tempC[0]), self.day_weather[day].pkt_dt

        return temp_date

    def lowest_temperature_day(self):
        temp_date = [999, -1]
        for day in self.day_weather:
            if self.day_weather[day].tempC[2] is not None:
                if int(self.day_weather[day].tempC[2]) < temp_date[0]:
                    temp_date = int(self.day_weather[day].tempC[2]), self.day_weather[day].pkt_dt

        return temp_date

    def max_humidity(self):
        humidity = [-1, -1]
        for day in self.day_weather:
            if self.day_weather[day].humidity[0] is not None:
                if int(self.day_weather[day].humidity[0]) > humidity[0]:
                    humidity = int(self.day_weather[day].humidity[0]), self.day_weather[day].pkt_dt

        return humidity

    def average_highest_temperature(self):

        s = 0
        count = 0

        for d in self.day_weather:
            if self.day_weather[d].tempC[0] is not None:
                s += int(self.day_weather[d].tempC[0])
                count += 1

        return s/count

    def average_lowest_temperature(self):

        s = 0
        count = 0

        for d in self.day_weather:
            if self.day_weather[d].tempC[2] is not None:
                s += int(self.day_weather[d].tempC[2])
                count += 1

        return s/count

    def average_mean_humidity(self):

        s = 0
        count = 0

        for d in self.day_weather:
            if self.day_weather[d].humidity[1] is not None:
                s += int(self.day_weather[d].humidity[1])
                count += 1

        return s / count
