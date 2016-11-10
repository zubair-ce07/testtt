from datetime import datetime


class WeatherData(object):

    def __init__(self, date,
                 max_temp=0,
                 mean_temp=0,
                 min_temp=0,
                 max_humidity=0,
                 mean_humidity=0,
                 min_humidity=0):

        self.date = datetime.strptime(date, '%Y-%m-%d')
        if max_temp:
            self.max_temp = float(max_temp)
        else:
            self.max_temp = 0

        if mean_temp:
            self.mean_temp = float(mean_temp)
        else:
            self.mean_temp = 0

        if min_temp:
            self.min_temp = float(min_temp)
        else:
            self.min_temp = 0

        if max_humidity:
            self.max_humidity = float(max_humidity)
        else:
            self.max_humidity = 0

        if mean_humidity:
            self.mean_humidity = float(mean_humidity)
        else:
            self.mean_humidity = 0

        if min_humidity:
            self.min_humidity = float(min_humidity)
        else:
            self.min_humidity = 0

    def __repr__(self):
        return 'Date=%s,Max Temperature=%s,' \
               'Mean_Temperature=%s,' \
               'Min_Temperature=%s,' \
               'Max_Humidity=%s,' \
               'Mean_Humidity=%s,' \
               'Min_Humidity=%s' % (self.date,
                                    self.max_temp,
                                    self.mean_temp,
                                    self.min_temp,
                                    self.max_humidity,
                                    self.mean_humidity,
                                    self.min_humidity)
