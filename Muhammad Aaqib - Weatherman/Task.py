import sys

class Weather:
    def __init__(self, pkt, max_temp, mean_temp, min_temp,
                 max_dew_point, mean_dew_point, min_dew_point,
                 max_humidity, mean_humidity, min_humidity,
                 max_sea_pressure, mean_sea_pressure, min_sea_pressure,
                 max_visibility, mean_visibility, min_visibility,
                 max_wind_speed, mean_wind_speed, max_gust_speed,
                precipitation, cloud_cover, events, wind_dir_degrees):      
        self.pkt = pkt
        self.max_temp = max_temp
        self.mean_temp = mean_temp 
        self.min_temp = min_temp
        self.max_dew_point = max_dew_point
        self.mean_dew_point = mean_dew_point
        self.min_dew_point = min_dew_point
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity 
        self.max_sea_pressure = max_sea_pressure
        self.mean_sea_pressure = mean_sea_pressure
        self.min_sea_pressure = min_sea_pressure
        self.max_visibility = max_visibility
        self.mean_visibility = mean_visibility 
        self.min_visibility = min_visibility
        self.max_wind_speed = max_wind_speed
        self.mean_wind_speed = mean_wind_speed
        self.max_gust_speed = max_gust_speed
        self.precipitation = precipitation
        self.cloud_cover = cloud_cover
        self.events = events
        self.wind_dir_degrees = wind_dir_degrees

    def set_pkt(self, pkt):
        self.pkt = pkt
    
    def set_max_temp(self, max_temp):
        self.max_temp = max_temp

    def set_mean_temp(self, mean_temp):
        self.mean_temp = mean_temp

    def set_min_temp(self, min_temp):
        self.min_temp = min_temp

    def set_max_dew_point(self, max_dew_point):
        self.max_dew_point = max_dew_point

    def set_mean_dew_point(self, mean_dew_point):
        self.mean_dew_point = mean_dew_point

    def set_min_dew_point(self, min_dew_point):
        self.min_dew_point = min_dew_point

    def set_max_humidity(self, max_humidity):
        self.max_humidity = max_humidity

    def set_mean_humidity(self, mean_humidity):
        self.mean_humidity = mean_humidity

    def set_min_humidity(self, min_humidity):
        self.min_humidity = min_humidity

    def set_max_sea_pressure(self, max_sea_pressure):
        self.max_sea_pressure = max_sea_pressure

    def set_mean_sea_pressure(self, mean_sea_pressure):
        self.mean_sea_pressure = mean_sea_pressure

    def set_min_sea_pressure(self, min_sea_pressure):
        self.min_sea_pressure = min_sea_pressure

    def set_max_visibility(self, max_visibility):
        self.max_visibility = max_visibility

    def set_mean_visibility(self, mean_visibility):
        self.mean_visibility = mean_visibility

    def set_min_visibility (self, min_visibility ):
        self.min_visibility  = min_visibility 

    def set_max_wind_speed(self, max_wind_speed):
        self.max_wind_speed = max_wind_speed

    def set_mean_wind_speed(self, mean_wind_speed):
        self.mean_wind_speed = mean_wind_speed

    def set_max_gust_speed(self, max_gust_speed):
        self.max_gust_speed = max_gust_speed

    def set_precipitation(self, precipitation):
        self.precipitation = precipitation

    def set_cloud_cover(self, cloud_cover):
        self.cloud_cover = cloud_cover

    def set_events(self, events):
        self.events = events

    def set_wind_dir_degrees(self, wind_dir_degrees):
        self.wind_dir_degrees = wind_dir_degrees

    
    def get_pkt(self):
        return self.pkt

    def get_max_temp(self):
        return self.max_temp

    def get_mean_temp(self):
        return self.mean_temp

    def get_min_temp(self):
        return self.min_temp

    def get_max_dew_point(self):
        return self.max_dew_point

    def get_mean_dew_point(self):
        return self.mean_dew_point

    def get_min_dew_point(self):
        return self.min_dew_point

    def get_max_humidity(self):
        return self.max_humidity

    def get_mean_humidity(self):
        return self.mean_humidity

    def get_min_humidity(self):
        return self.min_humidity

    def get_max_sea_pressure(self):
        return self.max_sea_pressure

    def get_mean_sea_pressure(self):
        return self.mean_sea_pressure

    def get_min_sea_pressure(self):
        return self.min_sea_pressure

    def get_max_visibility(self):
        return self.max_visibility

    def get_mean_visibility(self):
        return self.mean_visibility

    def get_min_visibility(self):
        return self.min_visibility

    def get_max_wind_speed (self):
        return self.max_wind_speed 

    def get_mean_wind_speed (self):
        return self.mean_wind_speed 

    def get_max_gust_speed (self):
        return self.max_gust_speed 

    def get_precipitation(self):
        return self.precipitation

    def get_cloud_cover(self):
        return self.cloud_cover

    def get_events(self):
        return self.events

    def get_wind_dir_degrees(self):
        return self.wind_dir_degrees


class YearCalculation:
    def __init__(self):
        self.max_year_temp = ""
        self.max_temp_pkt = ""
        self.min_year_temp = ""
        self.min_temp_pkt = ""
        self.max_year_humidity = ""
        self.max_humidity_pkt = ""
    
    def set_max_year_temp(self, max_year_temp):
        self.max_year_temp = max_year_temp
    
    def set_min_year_temp(self, min_year_temp):
        self.min_year_temp = min_year_temp

    def set_max_year_humidity(self, max_year_humidity):
        self.max_year_humidity = max_year_humidity
    
    def set_max_temp_pkt(self, max_temp_pkt):
        self.max_temp_pkt = max_temp_pkt
    
    def set_min_temp_pkt(self, min_temp_pkt):
        self.min_temp_pkt = min_temp_pkt
    
    def set_max_humidity_pkt(self, max_humidity_pkt):
        self.max_humidity_pkt = max_humidity_pkt

    
    def get_max_year_temp(self):
        return self.max_year_temp
    
    def get_min_year_temp(self):
        return self.min_year_temp

    def get_max_year_humidity(self):
        return self.max_year_humidity
    
    def get_max_temp_pkt(self):
        return self.max_temp_pkt

    def get_min_temp_pkt(self):
        return self.min_temp_pkt

    def get_max_humidity_pkt(self):
        return self.max_humidity_pkt


class MonthCalculation:
    def __init__(self):
        self.avg_max_temp = ""
        self.avg_min_temp = ""
        self.avg_mean_humidity = ""
    
    def set_avg_max_temp(self, avg_max_temp):
        self.avg_max_temp = avg_max_temp
    
    def set_avg_min_temp(self, avg_min_temp):
        self.avg_min_temp = avg_min_temp

    def set_avg_mean_humidity(self, avg_mean_humidity):
        self.avg_mean_humidity = avg_mean_humidity

    
    def get_avg_max_temp(self):
        return self.avg_max_temp
    
    def get_avg_min_temp(self):
        return self.avg_min_temp

    def get_avg_mean_humidity(self):
        return self.avg_mean_humidity


def check_month(date):
    a, b, c = date.split("-")
    del a
    del c
    if(b == "1"):
        return "January"
    if(b == "2"):
        return "February"
    if(b == "3"):
        return "March"
    if(b == "4"):
        return "April"
    if(b == "5"):
        return "May"
    if(b == "6"):
        return "June"
    if(b == "7"):
        return "July"
    if(b == "8"):
        return "August"
    if(b == "9"):
        return "September"
    if(b == "10"):
        return "October"
    if(b == "11"):
        return "November"
    else:
        return "December"

def parser():
    file_checker = [0 for i in range(13)]
    temp = {"Jan":"F", "Feb":"F", "Mar":"F", "Apr":"F", "May":"F",
            "Jun":"F", "Jul":"F", "Aug":"F", "Sep":"F", "Oct":"F",
            "Nov":"F", "Dec":"F"}
    for i in range(0, len(file_checker)):
        file_checker[i] = temp.copy()   
            
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
             "Sep", "Oct", "Nov", "Dec"]
    year = ["2004", "2005", "2006", "2007", "2008", "2009", "2010",
            "2011", "2012", "2013", "2014", "2015", "2016"]
    for i in range(0, len(year)):
        for j in range(0, len(month)):
            file_name = "weatherfiles/weatherfiles/Murree_weather_" + year[i] + "_" + month[j] + ".txt"
            try:
                infile = open(file_name, "r")
                file_checker[i][month[j]] = "T"
                infile.close()
            except:
                continue

    file_data = []
    for i in range(0, len(year)):
        temp_month_data = []
        for j in range(0, len(month)):
            temp_day_data = []
            if(file_checker[i][month[j]] == "T"):
                file_name = "weatherfiles/weatherfiles/Murree_weather_" + year[i] + "_" + month[j] + ".txt"
                infile = open(file_name, "r")
                line = infile.readline()
                for line in infile:
                    a, b, c, d, e, f, g, h, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y = line.split(",")
                    temp_day_data.append(Weather(a, b, c, d, e, f, g, h, k,
                                                 l, m, n, o, p, q, r, s, t,
                                                 u, v, w, x, y))
                temp_month_data.append(temp_day_data)
        file_data.append(temp_month_data)

    return file_data


def task_1(data, result, year):
    year_found = False
    index = 0
    for index in range(0, len(data[index])):
        time = data[index][0][0].get_pkt()
        a, b, c = time.split("-")
        del b
        if int(a) == int(year):
            year_found = True
            break
    if not year_found:
        print("Record of this year does not exist in system")
        return
    
    max_temp = data[index][0][0].get_max_temp()
    max_temp_pkt = data[index][0][0].get_pkt()
    for i in range(0, len(data[index])):
        for j in range(0, len(data[index][i])):
            if data[index][i][j].get_max_temp() == "":
                continue
            if int (data[index][i][j].get_max_temp()) > int (max_temp):
                max_temp = data[index][i][j].get_max_temp()
                max_temp_pkt = data[index][i][j].get_pkt()
    max_temp_day = check_month(max_temp_pkt)
    a, b, c = max_temp_pkt.split("-")
    print("Highest: " + max_temp + "C on " + max_temp_day + " " + c)

    min_temp = data[index][0][0].get_min_temp()
    min_temp_pkt = data[index][0][0].get_pkt()
    for i in range(0, len(data[index])):
        for j in range(0, len(data[index][i])):
            if data[index][i][j].get_min_temp() == "":
                continue
            if int (data[index][i][j].get_min_temp()) < int (min_temp):
                min_temp = data[index][i][j].get_min_temp()
                min_temp_pkt = data[index][i][j].get_pkt()
    min_temp_day = check_month(min_temp_pkt)
    a, b, c = min_temp_pkt.split("-")
    print("Lowest: " + min_temp + "C on " + min_temp_day + " " + c)

    max_humidity = data[index][0][0].get_max_humidity()
    max_humidity_pkt = data[index][0][0].get_pkt()
    for i in range(0, len(data[index])):
        for j in range(0, len(data[index][i])):
            if data[index][i][j].get_max_humidity() == "":
                continue
            if int (data[index][i][j].get_max_humidity()) > int (max_humidity):
                max_humidity = data[index][i][j].get_max_humidity()
                max_humidity_pkt = data[index][i][j].get_pkt()
    max_humidity_day = check_month(max_humidity_pkt)
    a, b, c = max_humidity_pkt.split("-")
    print("Humidity: " + max_humidity + "% on " + max_humidity_day + " " + c)


def task_2(data, result, month):
    year_found = False
    year, month = month.split("/")
    year_index = 0
    for year_index in range(0, len(data[year_index])):
        time = data[year_index][0][0].get_pkt()
        a, b, c = time.split("-")
        del c
        if int(a) == int(year):
            year_found = True
            break
    if not year_found:
        print("Record of this year does not exist in system")
        return

    month_found = False      
    for month_index in range(0, len(data[year_index])):
        time = data[year_index][month_index][0].get_pkt()
        a, b, c = time.split("-")
        if int(b) == int(month):
            month_found = True
            break
    if not month_found:
        print("Record of this month does not exist in system")
        return
 
    max_avg_temp = 0
    for i in range(0, len(data[year_index][month_index])):
        if data[year_index][month_index][i].get_max_temp() == "":
                continue
        max_avg_temp += int(data[year_index][month_index][i].get_max_temp())
    max_avg_temp = max_avg_temp / len(data[year_index][month_index])
    max_avg_temp = round(max_avg_temp, 2)
    print("Highest Average: " + str(max_avg_temp) + "C")
    #result.set_avg_max_temp(max_avg_temp)

    min_avg_temp = 0
    for i in range(0, len(data[year_index][month_index])):
        if data[year_index][month_index][i].get_min_temp() == "":
                continue
        min_avg_temp += int(data[year_index][month_index][i].get_min_temp())
    min_avg_temp = min_avg_temp / len(data[year_index][month_index])
    min_avg_temp = round(min_avg_temp, 2)
    print("Lowest Average: " + str(min_avg_temp) + "C")
    #result.set_avg_min_temp(min_avg_temp)

    mean_avg_humidity = 0
    for i in range(0, len(data[year_index][month_index])):
        if data[year_index][month_index][i].get_mean_humidity() == "":
                continue
        mean_avg_humidity += int(data[year_index][month_index][i].get_mean_humidity())
    mean_avg_humidity = mean_avg_humidity / len(data[year_index][month_index])
    mean_avg_humidity = round(mean_avg_humidity, 2)
    print("Average Mean Humidity: " + str(mean_avg_humidity) + "%")
    #result.set_avg_mean_humidity(mean_avg_humidity)


def task_3(data, month):
    temp = ""
    year_found = False
    year, month = month.split("/")
    year_index = 0
    for year_index in range(0, len(data[year_index])):
        time = data[year_index][0][0].get_pkt()
        temp = time
        a, b, c = time.split("-")
        del c
        if int(a) == int(year):
            year_found = True
            break
    if not year_found:
        print("Record of this year does not exist in system")
        return

    month_found = False      
    for month_index in range(0, len(data[year_index])):
        time = data[year_index][month_index][0].get_pkt()
        a, b, c = time.split("-")
        if int(b) == int(month):
            month_found = True
            break
    if not month_found:
        print("Record of this month does not exist in system")
        return
    
    print(check_month(temp) + " " + year)
    for i in range(0, len(data[year_index][month_index])):
        if i + 1 < 10:
            print(u"\u001b[35m0", end = "")
        print( u"\u001b[35m" + str(i + 1), end = " ")
        if data[year_index][month_index][i].get_max_temp() != "":
            for j in range(0, int(data[year_index][month_index][i].get_max_temp())):
                print( u"\u001b[31m+", end = "")
        print(u"\u001b[35m" + " " + data[year_index][month_index][i].get_max_temp() + "C")
        if i + 1 < 10:
            print(u"\u001b[35m0", end = "")
        print( u"\u001b[35m" + str(i + 1), end = " ")
        if data[year_index][month_index][i].get_min_temp() != "":
            for j in range(0, int(data[year_index][month_index][i].get_min_temp())):
                print( u"\u001b[36m+", end = "")
        print(u"\u001b[35m" + " " + data[year_index][month_index][i].get_min_temp() + "C")
        print()
