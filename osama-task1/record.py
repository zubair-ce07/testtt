from datetime import datetime


class Record:
    """ Represents a single weather record in the madrid csv file """

    def __init__(self,
                 date,
                 max_temp, mean_temp, min_temp,
                 max_dew, mean_dew, min_dew,
                 max_humidity, mean_humidity, min_humidity,
                 max_sea_pressure, mean_sea_pressure, min_sea_pressure,
                 max_visibility, mean_visibility, min_visibility,
                 max_wind_speed, mean_wind_speed,
                 max_gust_speed,
                 precipitation,
                 cloud_cover,
                 events,
                 wind_direction):
        """ Constructor function

        Keyword arguments:
        date -- datetime object (YYYY-MM-DD)
        max_temp, mean_temp, min_temp --  unit (Celsius)
        max_dew, mean_dew, min_dew -- unit (Celsius)
        max_humidity, mean_humidity, min_humidity -- value of humidity
        max_sea_pressure, mean_sea_pressure, min_sea_pressure -- unit (Pascal)
        max_visibility, mean_visibility, min_visibility -- unit (km)
        max_wind_speed, mean_wind_speed -- unit (km/h)
        max_gust_speed -- unit (km/h)
        precipitation -- unit (mm)
        cloud_cover -- unit (okta)
        events -- list of weather related eventsax
        wind_direction -- unit (degrees
        """
        self.date = datetime.strptime(' '.join(date.split('-')), "%Y %m %d").date()
        self.max_temp = int(max_temp) if max_temp.isdigit() else 0
        self.mean_temp = int(mean_temp) if mean_temp.isdigit() else 0
        self.min_temp = int(min_temp) if min_temp.isdigit() else 0
        self.max_dew = int(max_dew) if max_temp.isdigit() else 0
        self.mean_dew = int(mean_dew) if mean_temp.isdigit() else 0
        self.min_dew = int(min_dew) if min_temp.isdigit() else 0
        self.max_humidity = int(max_humidity) if max_humidity.isdigit() else 0
        self.mean_humidity = int(mean_humidity) if mean_humidity.isdigit() else 0
        self.min_humidity = int(min_humidity) if max_humidity.isdigit() else 0
        self.max_sea_pressure = int(max_sea_pressure)
        self.mean_sea_pressure = int(mean_sea_pressure)
        self.min_sea_pressure = int(min_sea_pressure)
        self.max_visibility = int(max_visibility) if max_visibility.isdigit() else 0
        self.mean_visibility = int(mean_visibility) if mean_visibility.isdigit() else 0
        self.min_visibility = int(min_visibility) if min_visibility.isdigit() else 0
        self.max_wind_speed = int(max_wind_speed)
        self.mean_wind_speed = int(mean_wind_speed)
        self.max_gust_speed = int(max_gust_speed) if max_gust_speed.isdigit() else 0
        self.precipitation = float(precipitation)
        self.cloud_cover = int(cloud_cover) if cloud_cover.isdigit() else 0
        self.events = events.split('-')
        self.wind_direction = int(wind_direction) if wind_direction.isdigit() else 0
    def __iter__(self):
        """ iterator method """
        return iter([self.date,
                     self.max_temp, self.mean_temp, self.min_temp,
                     self.max_dew, self.mean_dew, self.min_dew,
                     self.max_humidity, self.mean_humidity, self.min_humidity,
                     self.max_sea_pressure, self.mean_sea_pressure, self.min_sea_pressure,
                     self.max_visibility, self.mean_visibility, self.min_visibility,
                     self.max_wind_speed, self.mean_wind_speed, self.max_gust_speed,
                     self.precipitation, self.cloud_cover, self.events, self.wind_direction])

""" Utility functions """


def mean(numbers):
    """ returns the mean of a list of numbers """
    return int(sum(numbers)) / max(len(numbers), 1)