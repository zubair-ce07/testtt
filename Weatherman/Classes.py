import calendar


class Weather:

    def __init__(self, info):

        self.pkt = info[0]

        self.max_temp = info[1]
        self.mean_temp = info[2]
        self.min_temp = info[3]

        self.dew_point = info[4]
        self.mean_dew_point = info[5]
        self.min_dew_point = info[6]

        self.max_humidity = info[7]
        self.mean_humidity = info[8]
        self.min_humidity = info[9]

        self.max_sea_level_pressure = info[10]
        self.mean_Sea_Level_Pressure = info[11]
        self.min_Sea_Level_Pressure = info[12]

        self.max_visibility = info[13]
        self.mean_visibility = info[14]
        self.min_visibility = info[15]

        self.max_wind_speed = info[16]
        self.mean_wind_Speed = info[17]

        self.max_gust_speed = info[18]

        self.precipitation = info[19]

        self.cloud_cover = info[20]

        self.events = info[21]

        self.wind_dir_degrees = info[22]

    def get_month_day(self):

        date_list = str(self.pkt).split('-')

        month = calendar.month_abbr[int(date_list[1])]
        day = date_list[2]

        return month + " " + day

    def get_month_year(self):
        date_list = str(self.pkt).split('-')
        month = calendar.month_name[int(date_list[1])]
        year = date_list[0]

        return month + ' ' + year

    def get_day(self):
        date_list = str(self.pkt).split('-')
        return date_list[2]


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


