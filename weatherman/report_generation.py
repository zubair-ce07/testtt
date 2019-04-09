from calculations import Calculator

class  ReportGenerator:
    COLOR_BLUE = "\033[1;34;40m+"
    COLOR_RED = "\033[1;31;40m+"
    COLOR_WHITE = "\033[1;37;40m"        

    def print_averges(self, max_avg, min_avg, mean_humdity):
        
        print("\n---------------------------")   
        print(f'Highest Average:  {max_avg}C')
        print(f'Lowest Average:   {min_avg}C')
        print(f'Average Mean Humidity: {mean_humdity}%') 
        print("\n---------------------------")
            

    def print_graph(self, final_values, input_date):

        print(f'{input_date:%B }{input_date:%Y}')
        
        for value in final_values:
            self.draw_graph(value.date.day, value.max_temp, value.min_temp)

    def print_max(self, max_temp, min_temp, max_humidity):
        
        print("\n---------------------------")   
        print (f"Max temprature {max_temp.max_temp}C on {max_temp.date: %B} {max_temp.date.day}")
        print (f"Min temprature {min_temp.min_temp}C on {min_temp.date: %B} {min_temp.date.day}")
        print (f"Max Humidity {max_humidity.max_humidity}% on {max_humidity.date: %B} {max_humidity.date.day}")             
        print("\n---------------------------")
           
    def draw_graph(self, day, max_temp, min_temp):
        
        print(day, end=' ')
        print(self.COLOR_BLUE*min_temp, end='')
        print(self.COLOR_RED*max_temp, end='')
        print(f'{self.COLOR_WHITE} {min_temp}C', end=' ')
        print(f'{self.COLOR_WHITE} {max_temp}C')

