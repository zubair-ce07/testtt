class WeatherReport:

    def __init__ (self,max_temperature,min_temperature):
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature

    def max_temperature_graph(self,date):
        for max_temp_count in range(self.max_temperature):
            print('\033[91m'+'+',end='')

    def min_temperature_graph(self,date):
        for min_temp_count in range(self.min_temperature):
            print('\033[94m'+'+',end='')

    def merged_graph(self,date):
        print(date+' ',end='')
        self.max_temperature_graph(date)
        self.min_temperature_graph(date)
        print (' %dC - %dC'%(self.min_temperature,self.max_temperature))
