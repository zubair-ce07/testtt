"""
this module contain all classes
"""


class Temperature(object):
    """ class to store temperature data"""
    def __init__(self, max_temp, mean_temp, min_temp):
        self.max_temp = max_temp
        self.mean_temp = mean_temp
        self.min_temp = min_temp

    def to_string(self):
        """ return all members in a string """
        ret_str = "\n Max TemperatureC: " + str(self.max_temp)
        ret_str = ret_str + "\n Min TemperatureC: " + str(self.min_temp)
        ret_str = ret_str + "\n Mean TemperatureC: " + str(self.mean_temp)
        return ret_str

    def display(self):
        """ print all members """
        print(self.to_string())


class Dew(object):
    """ class to tore dew data """
    def __init__(self, dew, mean_dew, min_dew):
        self.dew = dew
        self.mean_dew = mean_dew
        self.min_dew = min_dew

    def to_string(self):
        """ return all members in a string """
        ret_str = "\n Dew PointC: " + str(self.dew)
        ret_str = ret_str + "\n Min DewpointC: " + str(self.min_dew)
        ret_str = ret_str + "\n MeanDew PointC: " + str(self.mean_dew)
        return ret_str

    def display(self):
        """ print all members """
        print(self.to_string())


class Humidity(object):
    """ class to store humidity data """
    def __init__(self, max_humidity, mean_humidity, min_humidity):
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity

    def to_string(self):
        """ return all members in a string """
        ret_str = "\n Max Humidity: " + str(self.max_humidity)
        ret_str = ret_str + "\n Min Humidity: " + str(self.min_humidity)
        ret_str = ret_str + "\n Mean Humidity: " + str(self.mean_humidity)
        return ret_str

    def display(self):
        """ print all members """
        print(self.to_string())


class SeaLevel(object):
    """ class to store sealevel data """
    def __init__(self, max_level, mean_level, min_level):
        self.max_level = max_level
        self.mean_level = mean_level
        self.min_level = min_level

    def to_string(self):
        """ return all members in a string """
        ret_str = "\n Max Sea Level PressurehPa: " + str(self.max_level)
        ret_str = (ret_str + "\n Min Sea Level " +
                   "PressurehPa: " + str(self.min_level))
        ret_str = (ret_str + "\n Mean Sea Level " +
                   "PressurehPa: " + str(self.mean_level))
        return ret_str

    def display(self):
        """ print all members """
        print(self.to_string())


class Visiblity(object):
    """ class to store visiblity data """
    def __init__(self, max_visiblity, mean_visiblity, min_visiblity):
        self.max_visiblity = max_visiblity
        self.min_visiblity = min_visiblity
        self.mean_visiblity = mean_visiblity

    def to_string(self):
        """ return all members in a string """
        ret_str = "\n Max VisibilityKm: " + str(self.max_visiblity)
        ret_str = ret_str + "\n Min VisibilityKm: " + str(self.min_visiblity)
        ret_str = ret_str + "\n Mean VisibilityKm: " + str(self.mean_visiblity)
        return ret_str

    def display(self):
        """ print all members """
        print(self.to_string())


class WindSpeed(object):
    """ class to store wind_speed data """
    def __init__(self, max_speed, mean_speed):
        self.max_speed = max_speed
        self.mean_speed = mean_speed

    def to_string(self):
        """ return all members in a string """
        ret_str = "\n Max Wind SpeedKm/h: " + str(self.max_speed)
        ret_str = ret_str + "\n Mean Wind SpeedKm/h" + str(self.mean_speed)
        return ret_str

    def display(self):
        """ print all members """
        print(self.to_string())


class DayRecord(object):
    """ class to store full day record """
    def __init__(self, date, temp, dew, humidity, sea_level,
                 visiblity, wind_speed, max_gust_speed,
                 precipitation, cloud_cover, event, wind_dir):
        self.date = date
        self.temp = temp
        self.dew = dew
        self.humidity = humidity
        self.sea_level = sea_level
        self.visiblity = visiblity
        self.wind_speed = wind_speed
        self.max_gust_speed = max_gust_speed
        self.precipitation = precipitation
        self.cloud_cover = cloud_cover
        self.event = event
        self.wind_dir = wind_dir

    def to_string(self):
        """ return all members in a string """
        ret_str = (self.temp.to_string() + self.dew.to_string() +
                   self.humidity.to_string() + self.sea_level.to_string() +
                   self.visiblity.to_string() + self.wind_speed.to_string() +
                   "\n Max Gust SpeedKm/h: " + str(self.max_gust_speed) +
                   "\n Precipitationmm: " + str(self.precipitation) +
                   "\n CloudCover: " + str(self.cloud_cover) +
                   "\n Events: " + self.event +
                   "\n WindDirDegrees: " + str(self.wind_dir))
        return ret_str

    def display(self):
        """ print all members """
        print(self.to_string())


class Count:
    """ strorage class to store total no of available records """
    def __init__(self, max_temp_count, min_temp_count, humidity_count):
        self.max_temp = max_temp_count
        self.min_temp = min_temp_count
        self.humidity = humidity_count

    def to_string(self):
        """ return all members in a string """
        ret_str = "\n total max_temp records count: " + str(self.max_temp)
        ret_str = (ret_str + "\n toal min_temp " +
                   "records count: " + str(self.min_temp))
        ret_str = (ret_str + "\n toal humidity " +
                   "records count: " + str(self.humidity))
        return ret_str

    def display(self):
        """ print all members """
        print(self.to_string())


class YearReport(object):
    """ contain module 1 ie year Report data """
    def __init__(self, max_temp, max_temp_date,
                 min_temp, min_temp_date,
                 humidity, humidity_date):
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.humidity = humidity
        self.max_temp_date = max_temp_date
        self.min_temp_date = min_temp_date
        self.humidity_date = humidity_date

    def to_string(self):
        """ return all members in a string """
        ret_str = (" Highest: " + str(self.max_temp) + "C on " +
                   (self.max_temp_date).strftime('%B %d') +
                   "\n Lowest: " + str(self.min_temp) + "C on " +
                   (self.min_temp_date).strftime('%B %d') +
                   "\n Humidity: " + str(self.humidity) + "% on " +
                   (self.humidity_date).strftime('%B %d'))
        return ret_str

    def display(self):
        """ print year report in correct syntax """
        year_str = str(self.max_temp_date.strftime('%Y'))
        if year_str != "1970":
            print(28 * "-", " YEAR REPORT_" + year_str + " ", 28 * "-")
            print(self.to_string())
            print((72 + len(year_str)) * "-", "\n")
        else:
            print("<< Invalid year -  Data is not available for given year\n")


class MonthReport(object):
    """ contain module 1 ie year Report data """
    def __init__(self, max_temp_sum, min_temp_sum, humidity_sum, count):
        self.max_temp_sum = max_temp_sum
        self.min_temp_sum = min_temp_sum
        self.humidity_sum = humidity_sum
        self.count = count

    def to_string(self):
        """ return all members in a string """
        ret_str = "\n total max_temp records sum: " + str(self.max_temp_sum)
        ret_str = (ret_str + "\n total min_temp " +
                   "records sum: " + str(self.min_temp_sum))
        ret_str = (ret_str + "\n total humidity " +
                   "records sum: " + str(self.humidity_sum))
        ret_str = ret_str + self.count.to_string()
        return ret_str

    def display(self):
        """ print all members """
        print(self.to_string())


class MonthAvgReport(object):
    """ contain month report """
    def __init__(self, max_temp_avg, min_temp_avg,
                 mean_humidity_avg, month_year):
        self.max_temp_avg = max_temp_avg
        self.min_temp_avg = min_temp_avg
        self.mean_humidity_avg = mean_humidity_avg
        self.month_year = month_year

    def to_string(self):
        """ return all members in a string """
        ret_str = (" Highest Average: " +
                   str(round(self.max_temp_avg, 2)) + "C" +
                   "\n Lowest Average: " +
                   str(round(self.min_temp_avg, 2)) + "C" +
                   "\n Average Mean Humidity: " +
                   str(round(self.mean_humidity_avg, 2)) + "%")
        return ret_str

    def display(self):
        """ display month_report average in correct syntax """
        print(28 * "-", " MONTH REPORT_" + self.month_year + " ", 28 * "-")
        print(self.to_string())
        print((73 + len(self.month_year)) * "-", "\n")
