import csv
from weather import howtocolor

def bonustask(name, path):

    fieldnames = ['PKT','Max TemperatureC','Mean TemperatureC','Min TemperatureC','Dew PointC','MeanDew PointC','Min DewpointC','Max Humidity', 'Mean Humidity', 'Min Humidity', 'Max Sea Level PressurehPa', 'Mean Sea Level PressurehPa', 'Min Sea Level PressurehPa', 'Max VisibilityKm', 'Mean VisibilityKm', 'Min VisibilitykM', 'Max Wind SpeedKm/h', 'Mean Wind SpeedKm/h', 'Max Gust SpeedKm/h','PrecipitationCm', 'CloudCover', 'Events','WindDirDegrees']

    max_list = []
    min_list = []
    avg_humidity = []

    csv_file = open(path +'/weathercsv/' + name +'.csv')
    csv_reader = csv.DictReader(csv_file, fieldnames)
    next(csv_reader)


    m=0
    for row in csv_reader:
        lineNum = csv_reader.line_num-2
        mintemp = row["Min TemperatureC"]
        print("{0:0=2d}".format(lineNum)," ",end ="")

        if mintemp is not None and mintemp is not "":
            for m in range(0, int(mintemp)):
                 howtocolor.prCyan("+", end="")

        maxtemp = row["Max TemperatureC"]

        if maxtemp is not None and maxtemp is not "":
            for m in range (0,int(maxtemp)):
                howtocolor.prRed("+", end = "")





        print(" ", "%2s" %mintemp, "C -", "%2s" %maxtemp, "C")

    csv_file.close()