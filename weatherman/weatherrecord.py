class WeatherRecord:

    def __init__(self, pkt='', max_temp=0, min_temp=0,
                 max_humidity=0, mean_humidity=0, month_name=''):

        self.pkt = pkt
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.month_name = month_name
