import datetime


class WeatherReadings:

    def __init__(self, row):

        if row.get('PKST'):
            self.pkt = row.get('PKST')

        if row.get('PKT'):
            self.pkt = row.get('PKT')

        self.max_temp = row.get('Max TemperatureC')
        self.mean_temp = row.get('Mean TemperatureC')
        self.min_temp = row.get('Min TemperatureC')

        self.dew_point = row.get('Dew PointC')
        self.mean_dew_point = row.get('MeanDew PointC')
        self.min_dew_point = row.get('Min DewpointC')

        self.max_humidity = row.get('Max Humidity')
        self.mean_humidity = row.get(' Mean Humidity')
        self.min_humidity = row.get(' Min Humidity')

        self.max_sea_level_pressure = row.get(' Max Sea Level PressurehPa')
        self.mean_Sea_Level_Pressure = row.get(' Mean Sea Level PressurehPa')
        self.min_Sea_Level_Pressure = row.get(' Min Sea Level PressurehPa')

        self.max_visibility = row.get(' Max VisibilityKm')
        self.mean_visibility = row.get(' Mean VisibilityKm')
        self.min_visibility = row.get(' Min VisibilityKm')

        self.max_wind_speed = row.get(' Max Wind SpeedKm/h')
        self.mean_wind_Speed = row.get(' Mean Wind SpeedKm/h')

        self.max_gust_speed = row.get(' Max Gust SpeedKm/h')

        self.precipitation = row.get('Precipitationmm')

        self.cloud_cover = row.get(' CloudCover')

        self.events = row.get(' Events')

        self.wind_dir_degrees = row.get('WindDirDegrees')

    def get_month_day(self):

        date_values = self.pkt.split('-')

        month_date = datetime.date(int(date_values[0]) , int(date_values[1]) , int(date_values[2]))

        return month_date.strftime("%B %d")                 # print(mydate.strftime("%A %d. %b %Y"))

    def get_month_year(self):

        date_values = self.pkt.split('-')

        month_date = datetime.date(int(date_values[0]), int(date_values[1]), int(date_values[2]))

        return month_date.strftime("%B %Y")

    def get_day(self):

        date_values = self.pkt.split('-')

        day = datetime.date(int(date_values[0]), int(date_values[1]), int(date_values[2]))

        return day.strftime("%d")


class YearlyWeatherReport:

    def __init__(self):

        self.highest_temp = 0
        self.highest_temp_day = ''

        self.lowest_temp = 0
        self.lowest_temp_day = ''

        self.highest_humidity = 0
        self.highest_humidity_day = ''

    def results(self):

        print 'Highest: {0}C on {1}'.format(self.highest_temp,self.highest_temp_day)
        print 'Lowest: {0}C on {1}'.format(self.lowest_temp, self.lowest_temp_day)
        print 'Humidity: {0}% on {1}'.format(self.highest_humidity, self.highest_humidity_day)
        print ' '


class MonthlyReport:

    days_count = 0

    def __init__(self):

        self.total_max_temp = 0
        self.total_min_temp = 0
        self.total_mean_humidity = 0

    def results(self):

        print 'Highest Average: {0}C'.format(self.total_max_temp / self.days_count)
        print 'Lowest Average: {0}C'.format(self.total_min_temp / self.days_count)
        print 'Average Mean Humidity: {0}%'.format(self.total_mean_humidity / self.days_count)
        print ' '

