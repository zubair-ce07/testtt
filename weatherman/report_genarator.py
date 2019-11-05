from file_reader import FileReader
from weather_calc import get_max_value, get_min_value
from weather_calc import get_average, highest_temp, lowest_temp
from file_helper import limit_float, merge_with_dates, replace_nulls
from file_helper import convert_int


month_lst = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
              'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


class WeatherEvaluator:
    def __init__(self, file_path, date = None):
        self.file_reader = FileReader(file_path, date)

    def yearly_report(self):
        print(f"\n    Yearly Report")

        max_tempratures = []
        maximum_temp = 0
        max_temp_date = ''

        min_tempratures = []
        minimum_temp = 100
        mini_temp_date = ''

        max_himidities = []
        maximum_himid = 0
        max_humid_date = ''
        
        for current_month in month_lst:
            temprature_list = []
            temprature_list = self.file_reader.get_yearly_record("Max TemperatureC", current_month)  
            if(temprature_list):
                max_tempratures.append(str(merge_with_dates(temprature_list)) + current_month)

        maximum_temp, max_temp_date = highest_temp(max_tempratures)


        for current_month in month_lst:
            temprature_list = []
            temprature_list = self.file_reader.get_yearly_record("Min TemperatureC", current_month)  
            if(temprature_list):
                min_tempratures.append(str(merge_with_dates(temprature_list)) + current_month)

        minimum_temp, min_temp_date = lowest_temp(min_tempratures)

        for current_month in month_lst:
            humid_list = []
            humid_list = self.file_reader.get_yearly_record(" Mean Humidity", current_month)  
            if(humid_list):
                max_himidities.append(str(merge_with_dates(humid_list)) + current_month)

        maximum_himid, max_humid_date = highest_temp(max_himidities)

        print(f'Highest: {maximum_temp}C on {max_temp_date}')
        print(f'Lowest: {minimum_temp}C on {min_temp_date}')
        print(f'Humidity: {maximum_himid}% on {max_humid_date}')
        
       #max_tempratures = self.file_reader.get_yearly_record("Max TemperatureC")    
        
    
    def monthly_average(self):
        print(f"\n    Monthly Average Report")
        mean_temp_list = self.file_reader.get_record("Mean TemperatureC")
        mean_humid_list = self.file_reader.get_record(" Mean Humidity")
        
        if(mean_temp_list): 
            avg_highest_temp = get_max_value (mean_temp_list)
            avg_lowest_temp = get_min_value(mean_temp_list)
            avg_mean_humid = limit_float(get_average(mean_humid_list))
            
            print(f'Highest Average:{avg_highest_temp}C')
            print(f'Lowest Average:{avg_lowest_temp}C')
            print(f'Average Mean Humidity:{avg_mean_humid}%')
            
        else:
            print('file does not exist')    
    
    def horizontal_bar(self):
        print(f"\n    Horizontal Bar Report")
        max_temp_list = self.file_reader.get_record("Max TemperatureC")
        min_temp_list = self.file_reader.get_record("Min TemperatureC")
        
        max_temp_list = convert_int(replace_nulls(max_temp_list))
        min_temp_list = convert_int(replace_nulls(min_temp_list))
        
        if(max_temp_list): 
            for i in range(len(max_temp_list)):
                if i < 9:
                    print(f"\n0" + str(i+1), end=" ")
                else:
                    print(f"\n" + str(i+1), end=" ")

                for j in range(min_temp_list[i]):
                    print(f'\033[1;34m' '+' '\033[1;m', end=" ")

                for j in range(max_temp_list[i]):
                    print(f'\033[31m' '+' '\033[0m', end=" ")
                print(f'{max_temp_list[i]}C - {min_temp_list[i]}C')
        else:
            print('file does not exist')