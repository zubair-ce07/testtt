import csv


def task2(name,path):

    fieldnames = ['PKT','Max TemperatureC','Mean TemperatureC','Min TemperatureC','Dew PointC','MeanDew PointC','Min DewpointC','Max Humidity', 'Mean Humidity', 'Min Humidity', 'Max Sea Level PressurehPa', 'Mean Sea Level PressurehPa', 'Min Sea Level PressurehPa', 'Max VisibilityKm', 'Mean VisibilityKm', 'Min VisibilitykM', 'Max Wind SpeedKm/h', 'Mean Wind SpeedKm/h', 'Max Gust SpeedKm/h','PrecipitationCm', 'CloudCover', 'Events','WindDirDegrees']

    max_list = []
    min_list = []
    avg_humidity = []

    csv_file = open(path +'/weathercsv/' + name +'.csv')
    csv_reader = csv.DictReader(csv_file, fieldnames)
    next(csv_reader)

    for row in csv_reader:
        maxtemp = row["Max TemperatureC"]
        if maxtemp is not None and maxtemp is not "":
            max_list.append(float(row["Max TemperatureC"]))

        mintemp = row["Min TemperatureC"]
        if mintemp is not None and mintemp is not "":
            min_list.append(float(row["Min TemperatureC"]))

        avghumidity = row["Mean Humidity"]
        if avghumidity is not None and avghumidity is not "":
            avg_humidity.append(float(row["Mean Humidity"]))


    avg_maxtemp = sum(max_list)/len(max_list)
    print("Highest Average:  ", "%.1f" %avg_maxtemp,"C")

    avg_mintemp = sum(min_list)/len(min_list)
    print("Lowest Average:  ", "%.1f" %avg_mintemp,"C")

    avg_avghumidity = sum(avg_humidity)/len(avg_humidity)
    print("Average Humidity:  ", "%.1f" %avg_avghumidity,"%")


    csv_file.close()