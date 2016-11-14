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
        self.max_temp = float(max_temp) if max_temp else 0
        self.mean_temp = float(mean_temp) if mean_temp else 0
        self.min_temp = float(min_temp) if min_temp else 0
        self.max_humidity = float(max_humidity) if max_humidity else 0
        self.mean_humidity = float(mean_humidity) if mean_humidity else 0
        self.min_humidity = float(min_humidity) if min_humidity else 0
        
    def __repr__(self):
        return 'Date=%s,Max Temperature=%s,' \
               'Mean_Temperature=%s,' \
               'Min_Temperature=%s,' \
               'Max_Humidity=%s,' \
               'Mean_Humidity=%s,' \
               'Min_Humidity=%s'.format(self.date,
                                        self.max_temp,
                                        self.mean_temp,
                                        self.min_temp,
                                        self.max_humidity,
                                        self.mean_humidity,
                                        self.min_humidity)
