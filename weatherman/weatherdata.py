import calendar


class WeatherData:

    def __init__(self, pkt='', max_temp=0, mean_temp=0, min_temp=0,
                 max_humidity=0, mean_humidity=0, min_humidity=0):

        self.pkt = pkt
        self.max_temp = max_temp
        self.mean_temp = mean_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity
        self.year = pkt[0:4]
        self.month_index = int(pkt[5:7].replace('-', ''))
        self.month_name = calendar.month_name[int(pkt[5:7].replace('-', ''))]
        self.day = int(pkt[7:].replace('-', ''))
