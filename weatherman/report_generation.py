from calculations import Calculator
import statistics
import datetime

class  Printer:


    def print_averges(self, all_data, input_date):
        c = Calculator()
        max_avg, min_avg, mean_humdity = c.calculating_averages(all_data, input_date)
        print("\n---------------------------")   
        print(f'Highest Average:  {max_avg}C')
        print(f'Lowest Average:   {min_avg}C')
        print(f'Average Mean Humidity: {mean_humdity}%') 
        print("\n---------------------------")
            

    def print_graph(self, all_data, input_date):
        c = Calculator()
        final = c.getting_min_max(all_data, input_date)
        date = datetime.datetime.strptime(str(input_date), '%Y-%m-%d').date()
        print(f'{input_date:%B }{input_date:%Y}')
        for key in final:
            date = datetime.datetime.strptime(key[0], '%Y-%m-%d').day
            self.draw_graph(date, key[1], key[2])


    def print_max(self, all_data, inputt):
        c = Calculator()
        max_temp, min_temp, max_humidity = c.getting_temperatures(all_data, inputt)
        
        print("\n---------------------------")   
        date = datetime.datetime.strptime(max_temp[-1][0], '%Y-%m-%d').date()
        print (f"Max temprature {max_temp[-1][1]}C on {date: %B} {date.day}")
        
        date = datetime.datetime.strptime(min_temp[0][0], '%Y-%m-%d').date()
        print (f"Min temprature {min_temp[0][1]}C on {date: %B} {date.day}")
        
        date = datetime.datetime.strptime(max_humidity[-1][0], '%Y-%m-%d').date()
        print (f"Max Humidity   {max_humidity[-1][1]}% on {date: %B} {date.day}")             
        print("\n---------------------------")
            
    
    def draw_graph(self, day, max_temp, min_temp):
        print(day, end=' ')

        for i in range(int(min_temp)):
            print("\033[1;34;40m+", end='')     
        
        for i in range(int(max_temp)):
            print("\033[1;31;40m+", end='')
        print(f'\033[1;37;40m {min_temp}C', end=' ')
        print(f'\033[1;37;40m {max_temp}C')
