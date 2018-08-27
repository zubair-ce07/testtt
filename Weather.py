class Weather:

    """Holds the Weather Data"""

    def __init__(self):
        self.pkt_dt = None
        self.tempC = []
        self.dew_pointC = []
        self.humidity = []
        self.sea_level_pressurehPa = []
        self.visibilitykm = []
        self.winde_speedkmph = []
        self.max_gust_speedkmph = 0
        self.percipitaionmm = 0
        self.cloud_cover = 0
        self.event = ""
        self.wind_directionD = 0



