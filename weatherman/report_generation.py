import calculations as cal
import statistics
import datetime


def date_splitter(date):
    day = str(datetime.datetime.strptime(date, '%Y-%m-%d').day)
    year = str(datetime.datetime.strptime(date, '%Y-%m-%d').year)
    month = datetime.datetime.strptime(date, '%Y-%m-%d')
    month = month.strftime("%B")
    return (str(day), str(month), year)


def print_averges(max_temp, min_temp, mean_humd):
    highest_temp_average = round(statistics.mean(max_temp)) 
    lowest_temp_average = round(statistics.mean(min_temp))
    mean_humd_average = round (statistics.mean(mean_humd))

    print("\n---------------------------")   
    print(f'Highest Average:  {highest_temp_average}C')
    print(f'Lowest Average:   {lowest_temp_average}C')
    print(f'Average Mean Humidity: {mean_humd_average}%') 
    print("\n---------------------------")


def print_graph(max_temp, min_temp,year_month):
    (day, month, year) = date_splitter(str(year_month))
    print (f'{month} {year}')    
    print("\n")
    for key in (max_temp):
            cal.draw_graph(key, max_temp[key], min_temp[key])

    print("\n---------------------------")


def print_max(max_temp, min_temp, max_humd):
    (day, month, year) = date_splitter(max_temp['date'])
    print (f"Max temprature {max_temp['MaxTemp']}C  on {day} {month}")
    
    (day, month, year) = date_splitter(min_temp['date'])
    print (f"Min temprature {min_temp['MinTemp']}C  on {day} {month}")
    
    (day, month, year) = date_splitter(max_humd['date'])
    print (f"Max Humidity   {max_humd['MaxHumd']}%  on {day} {month}")             
    print("\n---------------------------")


