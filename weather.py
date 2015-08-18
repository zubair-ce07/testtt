class Weather:
  
    def __init__(self, max_temp = 0, min_temp = 0, max_hum = 0, min_hum = 0, hot_day = "", cool_day = "", year = 0):
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_hum = max_hum
        self.min_hum = min_hum
        self.hot_day = hot_day
        self.cool_day = cool_day
        self.year = year
    

    def displayEmployee(self):
        print "Maximum Temperature : ", self.max_temp,  ", Minimun Temperature : ", self.min_temp,   ", Minimun Humidity : ", self.min_hum,   ", Maximun Humidity : ", self.max_hum,   ", Hottest Day : ", self.hot_day,   ", Coolest Day : ", self.cool_day