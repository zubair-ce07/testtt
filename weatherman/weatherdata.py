import calendar


class WeatherData:
    """
    WeatherData holds all the necessary properties and methods for
    report generation.
    """

    def __init__(self, pkt='', max_temp=0, mean_temp=0, min_temp=0,
                 max_humidity=0, mean_humidity=0, min_humidity=0):

        """
        Constructor function

        Arguments:
            pkt (str): Date in string format
            max_temp (int): Maximum Temperature
            mean_temp (int): Mean Temperature
            min_temp (int): Mininmum Temperature
            max_humidity (int): Maximum Humidity
            mean_humidity (int): Mean Humidity
            min_humidity (int): Minimum Humidity
        """

        self.pkt = pkt
        self.max_temp = max_temp
        self.mean_temp = mean_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity

        # format of pkt is 2004-8-1
        self.year = pkt[0:4]
        self.month_index = int(pkt[5:7].replace('-', ''))
        self.month_name = calendar.month_name[int(pkt[5:7].replace('-', ''))]
        self.day = int(pkt[7:].replace('-', ''))
