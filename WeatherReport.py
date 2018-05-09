class WeatherReport:

    def __init__ (self,max_temperature,min_temperature):
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature

    def max_temperature_graph(self,date):
        print('\033[91m'+'+'*self.max_temperature,end='')

    def min_temperature_graph(self,date):
        print('\033[94m'+'+'*self.min_temperature,end='')

    def merged_graph(self,date):
        print(date+' ',end='')
        self.min_temperature_graph(date)
        self.max_temperature_graph(date)
        print (' %dC - %dC'%(self.min_temperature,self.max_temperature))
