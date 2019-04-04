import calculations as cal
import statistics


def print_averges(max_temp, min_temp, mean_humd):
    highest_temp_average = round(statistics.mean(max_temp)) 
    lowest_temp_average = round(statistics.mean(min_temp))
    mean_humd_average = round (statistics.mean(mean_humd))

    print("\n---------------------------")   
    print(f'Highest Average:  {highest_temp_average}C')
    print(f'Lowest Average:   {lowest_temp_average}C')
    print(f'Average Mean Humidity: {mean_humd_average}%') 
    print("\n---------------------------")


def print_graph(max_temp, min_temp):
    for key in (max_temp):
            cal.draw_graph(key, max_temp[key], min_temp[key])

    print("\n---------------------------")


def print_max(max_temp, min_temp, max_humd):
    print("\n---------------------------")
    print (f"Max temprature {max_temp['MaxTemp']}  on {max_temp['date']}")
    print (f"Min temprature {min_temp['MinTemp']}  on {min_temp['date']}")
    print (f"Max Humidity   {max_humd['MaxHumd']}  on {max_humd['date']}")             
    print("\n---------------------------")

