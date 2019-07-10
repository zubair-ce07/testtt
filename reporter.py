from colorama import Fore
from colorama import Style
import math


def yearly_report(per_year_records, input_data):
    """This function will print max temperature, max humidity and minimum temperature in 
    in the year details.
    """

    try:
        print ("In Year: ", input_data)
        print ("Highest: " + per_year_records[input_data]['Highest: '])
        print ("Lowest: " + per_year_records[input_data]['Lowest: '])
        print ("Humidity: " + per_year_records[input_data]['Humidity: '])
    except:
        print ("Invalid Input....")
    return None


def monthly_report(years_monthly_records, input_data, months):
    """This will report highest average temperature, lowest average temperature and average mean humidity."""


    input_data = input_data.split('/')
    month = months[int(input_data[1])-1]

    for an_year in years_monthly_records:
        if an_year[0] == input_data[0]:
            for a_month in an_year:
                if a_month[0] == month:

                    print (
                        "Highest Average: " 
                        + str(int(a_month[2])) + "C")
                    print (
                        "Lowest Average: " 
                        + str(int(a_month[6])) + "C")
                    print (
                        "Average Mean Humidity: " 
                        + str(int(a_month[11])) + "%")
    return None


def monthly_bar_chart(years_monthly_records, input_data, months):
    """This will print the bar chart."""


    input_data = input_data.split('/')
    month = months[int(input_data[1])-1]

    for an_year in years_monthly_records:
        if an_year[0] == input_data[0]:
            for a_month in an_year:
                if a_month[0] == month:

                    highest_temps = a_month[4]
                    lowest_temps = a_month[8]
                    print (month, ' ', input_data[0])
                    
                    for a,b in zip(
                    
                        range(len(highest_temps)), range(len(lowest_temps))):
                    
                        if highest_temps[a] != -math.inf:
                    
                            s = highest_temps[a] * "+"
                            cred = '\033[91m'
                            cend = '\033[0m'
                            violet = '\33[4m'
                            print (
                                violet + str(a+1) 
                                + cend + ' ' + cred 
                                + s + cend + " " 
                                + str(highest_temps[a]) + 'C')
                        
                        if lowest_temps[b] != math.inf:
                    
                            s = lowest_temps[b] * "+"
                            cred = '\33[34m'
                            cend = '\033[0m'
                            violet = '\33[4m'
                            print (
                                violet + str(b+1) + cend 
                                + ' ' + cred + s + cend 
                                + ' ' + str(lowest_temps[b]) + 'C')
                    break
    return None


def horizontal_barchart(years_monthly_records, input_data, months):
    """This will print horizontal bar chart."""


    input_data = input_data.split('/')
    month = months[int(input_data[1])-1]
    
    for an_year in years_monthly_records:
        if an_year[0] == input_data[0]:
            for a_month in an_year:
                if a_month[0] == month:

                    highest_temps = a_month[4]
                    lowest_temps = a_month[8]
                    print (month, ' ', input_data[0])
                    
                    for a,b in zip(
                    
                        range(len(highest_temps)), range(len(lowest_temps))):
                        
                        if highest_temps[a] != -math.inf and lowest_temps[b] != math.inf:
                            
                            s = highest_temps[a] * "+"
                            s2 = lowest_temps[b] * '+'
                            cred = '\033[91m'
                            cblue = '\33[34m'
                            cend = '\033[0m'
                            violet = '\33[4m'
                            print (
                                str(a+1) + ' ' + cblue 
                                + s2 + cend + cred + s 
                                + cend + " " + str(lowest_temps[b]) 
                                + 'C-' + str(highest_temps[a]) + 'C')
                    break
    return None