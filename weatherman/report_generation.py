import calculations as cl
import datetime

def extracting_date(date):
        x = date.split("-")
        day = x[2]
        return day


def date_splitter(dates_string): 
    x = dates_string.split("-")
    new_list = list(map(int, x))
    temp_date = datetime.datetime(new_list[0], new_list[1], new_list[2])
    final_date = temp_date.strftime("%b %d")
    
    return final_date


def print_averges(final_list):
    averrage_highest = cl.calculating_average(final_list, 1)
    averrage_lowest = cl.calculating_average(final_list, 3)
    averrage_humidity = cl.calculating_average(final_list, 7)
    #print(f"Average Highest: " + str(averrage_highest) + " C")
    print(f"Average Highest: {averrage_highest} C")
    
    print(f"Average Lowst: {averrage_lowest}   C")
    print(f"Average Humidit: {averrage_humidity} %")
    
    print("\n-----------------------")


def print_graph(all_days):
    for i in range(len(all_days)-1):
        if all_days[i][1] != '' or all_days[i][3] != '' or all_days[i][7] != '':
                cl.draw_graph(extracting_date(all_days[i][0]), all_days[i][1], all_days[i][3])
                print("\n")    


def print_max(sorted_data):
    print("\n-----------------------")

    final_date = date_splitter(str(sorted_data[0][0]))
    print(f"Max Temprature:  {sorted_data[0][1]}  C on {final_date}")         
    final_date = date_splitter(str(sorted_data[1][0]))
    print(f"Min temprature: {sorted_data[1][3]} C on {final_date}")
    final_date = date_splitter(str(sorted_data[2][0]))
    print(f"Max Humidity:  {sorted_data[2][7]} %   on  {final_date}")
    print("\n-----------------------")

