class Weather:
  
    def __init__(self, max_temp = '', min_temp = '', max_hum = '', min_hum = '', date = "", year = 0):
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_hum = max_hum
        self.min_hum = min_hum
        self.date = date
        self.year = year
    

    def displayWeather(self):
        print "Maximum Temperature : ", self.max_temp,  ", Minimun Temperature : ", self.min_temp,   ", Minimun Humidity : ", self.min_hum,   ", Maximun Humidity : ", self.max_hum,   ", Date : ", self.date