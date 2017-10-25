import datetime
import operator


class WeatherReading:

    def __init__(self, row):

        if 'PKST' in row:
            self.pkt = row.get('PKST')
        else:
            self.pkt = row.get('PKT')

        self.weather_date = self.pkt.split('-')
        self.year = int(self.weather_date[0])
        self.month = int(self.weather_date[1])
        self.day = int(self.weather_date[2])

        if row.get('Max TemperatureC'):
            self.max_temp = int(row.get('Max TemperatureC'))
        else:
            self.max_temp = row.get('Max TemperatureC')
        self.mean_temp = row.get('Mean TemperatureC')

        if row.get('Min TemperatureC'):
            self.min_temp = int(row.get('Min TemperatureC'))
        else:
            self.min_temp = row.get('Min TemperatureC')

        self.dew_point = row.get('Dew PointC')
        self.mean_dew_point = row.get('MeanDew PointC')
        self.min_dew_point = row.get('Min DewpointC')

        if row.get('Max Humidity'):
            self.max_humidity = int(row.get('Max Humidity'))
        else:
            self.max_humidity = row.get('Max Humidity')

        if row.get(' Mean Humidity'):
            self.mean_humidity = int(row.get(' Mean Humidity'))
        else:
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

        month_date = datetime.date(self.year , self.month , self.day)

        return month_date.strftime("%B %d")                 # print(mydate.strftime("%A %d. %b %Y"))

    def get_month_year(self):

        date_values = self.pkt.split('-')

        month_date = datetime.date(self.year , self.month , self.day)

        return month_date.strftime("%B %Y")

    def get_day(self):

        date_values = self.pkt.split('-')

        day = datetime.date(self.year , self.month , self.day)

        return day.strftime("%d")


class YearlyWeatherReport:

    def __init__(self):

        self.complete_records = []

    def print_report(self):

        new_records = [row for row in self.complete_records if row.max_temp]
        required_record = max(new_records, key=lambda row: row.max_temp)

        print "Highest: {0}C on {1}".format(required_record.max_temp, required_record.get_month_day())

        new_records = [row for row in self.complete_records if row.min_temp]
        required_record = min(new_records, key=lambda row: row.min_temp)

        print "Lowest: {0}C on {1}".format(required_record.min_temp, required_record.get_month_day())

        new_records = [row for row in self.complete_records if row.max_humidity]
        required_record = max(new_records, key=lambda row: row.max_humidity)

        print "Humidity: {0}% on {1} \n".format(required_record.max_humidity, required_record.get_month_day())


class MonthlyReport:

    days_count = 0

    def __init__(self):

        self.total_max_temp = 0
        self.total_min_temp = 0
        self.total_mean_humidity = 0

    def print_report(self):

        print 'Highest Average: {0}C'.format(self.total_max_temp / self.days_count)
        print 'Lowest Average: {0}C'.format(self.total_min_temp / self.days_count)
        print 'Average Mean Humidity: {0}%'.format(self.total_mean_humidity / self.days_count)
        print ' '

