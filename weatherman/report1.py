import os.path
from reportlab.pdfgen import canvas

month_lst = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
              'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def Report(fpath):
    print("\n    Report 1")
    max_temp = 0
    max_temp_month = 0

    min_temp = 200
    min_temp_month = 0

    max_humid = 0
    max_humid_month = 0
    
    for month in range(12):
        
        my_file = fpath + "_" + month_lst[month] + ".txt"
        temprature_list = []
        humidity_list = []

        if os.path.isfile(my_file): 
            with open(my_file) as file:
                next(file)             #skip first line of the file
                # Values of temprature and humidity inserted into perticular list
                for line in file:
                    file = line.split(',')
                    temprature_list.append(file[2])
                    humidity_list.append(file[8])
    
            while '' in temprature_list:
                temprature_list.remove('')
            while '' in humidity_list:
                humidity_list.remove('')    
            
            temprature_list = list(map(int, temprature_list)) 
            humidity_list = list(map(int, humidity_list))

            if len(temprature_list) != 0 and max_temp < max(temprature_list):
                max_temp = max(temprature_list)
                max_temp_month = month
                
            if len(temprature_list) != 0 and min_temp > min(temprature_list):    
                min_temp = min(temprature_list)
                min_temp_month = month

            if len(humidity_list) != 0 and max_temp < max(humidity_list):
                max_humid = max(humidity_list)
                max_humid_month = month    

            
    print("Highest: " + str(max_temp) + "C on " + month_lst[max_temp_month])   
    print("Lowest: " + str(min_temp) + "C on " + month_lst[min_temp_month])
    print("Humidity: " + str(max_humid) + "% on " + month_lst[max_humid_month])


    # Genarates report
    c = canvas.Canvas("Report1.pdf")
    c.drawString(150, 700, "Highest: " + str(max_temp) + "C on " + month_lst[max_temp_month])
    c.drawString(150, 685, "Lowest: " + str(min_temp) + "C on " + month_lst[min_temp_month])
    c.drawString(150, 670, "Humidity: " + str(max_humid) + "% on " + month_lst[max_humid_month])
    c.save()