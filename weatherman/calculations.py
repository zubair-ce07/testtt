import datetime
import statistics
import csv
import glob


def getting_year(date):
    return str(datetime.datetime.strptime(date, '%Y-%m-%d').year)


def getting_day(date):
    return str(datetime.datetime.strptime(date, '%Y-%m-%d').day)


def getting_year_month(date):
    year = str(datetime.datetime.strptime(date, '%Y-%m-%d').year)
    month = str(datetime.datetime.strptime(date, '%Y-%m-%d').month)
    return (year, month)


def get_files(basepath):
    files = glob.glob(f'{basepath}{"/"}{"*.txt"}')
    return files


def getting_max(files, final_max_temp, final_min_temp, final_max_humd, year):
    temp = None
    max_temp = None
    max_date = None
    min_temp = None
    min_date = None
    max_humd = None
    max_h_date = None
    input_file = csv.DictReader(open(files))
    for row in input_file:
            if "PKT" in row.keys():
                if getting_year(row["PKT"]) == str(year):
                    if row["Max TemperatureC"] != '':
                        temp = int(row["Max TemperatureC"])
                        if  max_temp is None or max_temp < temp:
                            max_temp = temp
                            max_date = row["PKT"]
                        
                        if row["Min TemperatureC"] != '':
                            temp2 = int(row["Min TemperatureC"])
                            if min_temp is None or min_temp > temp2:
                                min_temp = temp2
                                min_date = row["PKT"]
                        
                        if row["Max Humidity"] != '':
                            temp3 = int(row["Max Humidity"])
                            if max_humd is None or max_humd < temp3:
                                max_humd = temp3
                                max_h_date = row["PKT"]
                        
                        if max_temp > int(final_max_temp['MaxTemp']):
                            final_max_temp['MaxTemp'] = max_temp
                            final_max_temp['date'] = max_date
                        
                        if min_temp < int(final_min_temp['MinTemp']):
                            final_min_temp['MinTemp'] = min_temp
                            final_min_temp['date'] = min_date
                        
                        if max_humd > int(final_max_humd['MaxHumd']):
                            final_max_humd['MaxHumd'] = max_humd
                            final_max_humd['date'] = max_h_date
            
    return (final_max_temp, final_min_temp, final_max_humd)


def calculating_averages(files, year_month, max_temp, min_temp, max_humd):
     (year,month)=getting_year_month(str(year_month))
     input_file=csv.DictReader(open (files))
     for row in input_file:
            if "PKT" in row.keys():
                if getting_year_month(row["PKT"]) == (year, month):
                         for row in input_file:
                             max_temp.append(row["Max TemperatureC"])
                             min_temp.append(row["Min TemperatureC"])
                             max_humd.append(row[" Mean Humidity"])

     max_temp=[int(t) for t in max_temp if t]
     min_temp=[int(t) for t in min_temp if t]
     max_humd=[int(t) for t in max_humd if t]

     return (max_temp, min_temp, max_humd)

def getting_temperatures(files,year_month,max_temp,min_temp):
     
     (year,month)=getting_year_month(str(year_month))
     input_file=csv.DictReader(open (files))
     for row in input_file:
            if "PKT" in row.keys():
                if getting_year_month(row["PKT"]) == (year, month):
                         for row in input_file:
                             if row["Max TemperatureC"] != '' and row["Min TemperatureC"] != '':
                                max_temp[getting_day(row["PKT"])] = row["Max TemperatureC"]
                                min_temp[getting_day(row["PKT"])] = row["Min TemperatureC"]

     return (max_temp, min_temp)


def draw_graph(day, max_temp, min_temp):
    print(day, end=' ')                      
    for i in range(int(min_temp)):
        print("\033[1;34;40m+", end='')     
    for i in range(int(max_temp)):
        print("\033[1;31;40m+", end='')
    print("\033[1;37;40m" + str(min_temp) + "C", end=' ')
    print("\033[1;37;40m" + str(max_temp) + "C")
