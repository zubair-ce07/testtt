from datetime import datetime


class WeatherData:

    def __init__(self, date, highest_temp, lowest_temp, highest_humidity, avg_humidity):

        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.highest_temp = int(highest_temp) if highest_temp.isdigit() else highest_temp
        self.lowest_temp = int(lowest_temp) if lowest_temp.isdigit() else lowest_temp
        self.highest_humidity = int(highest_humidity) if highest_humidity.isdigit() else highest_humidity
        self.avg_humidity = int(avg_humidity) if avg_humidity.isdigit() else avg_humidity

