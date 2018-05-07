class WeatherReport:

    def __init__ (self,max_temperature,min_temperature):
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature

    def printGraphForMaxTemperature(self,date):                              #creates graph for max temperature
        for max_temp_count in range(self.max_temperature):
            print('\033[91m'+'+',end='')


    def printGraphForMinTemperature(self,date):                              #creates graph for min temperature
        for min_temp_count in range(self.min_temperature):
            print('\033[94m'+'+',end='')


    def printMinMaxTemperatureGraphForDay(self,date):    #creates merged graph for max and min temperature
        print(date+' ',end='')
        self.printGraphForMinTemperature(date)
        self.printGraphForMaxTemperature(date)
        print (' %dC - %dC'%(self.min_temperature,self.max_temperature))
