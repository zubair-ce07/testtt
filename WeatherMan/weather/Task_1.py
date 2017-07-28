import csv
import glob
import operator
import datetime

def task1(year,path):


    fieldnames = ['PKT','Max TemperatureC','Mean TemperatureC','Min TemperatureC','Dew PointC','MeanDew PointC','Min DewpointC','Max Humidity', 'Mean Humidity', 'Min Humidity', 'Max Sea Level PressurehPa', 'Mean Sea Level PressurehPa', 'Min Sea Level PressurehPa', 'Max VisibilityKm', 'Mean VisibilityKm', 'Min VisibilitykM', 'Max Wind SpeedKm/h', 'Mean Wind SpeedKm/h', 'Max Gust SpeedKm/h','PrecipitationCm', 'CloudCover', 'Events','WindDirDegrees']

    max_temp = []
    min_temp = []
    hu_mid = []
    month_date = []
    date = []
    i=0


    files = [file for file in glob.glob(path +'/weathercsv/' + year +'/*.csv', recursive=True)]
    #print(files)

    for i in files:
        #print(i)
        csv_file = open(i)
        csv_reader = csv.DictReader(csv_file, fieldnames)
        next(csv_reader)

        for row in csv_reader:

            maxtemp = row["Max TemperatureC"]
            month_date = row["PKT"]

            if maxtemp is not None and maxtemp is not "":
                max_temp.append(float(row["Max TemperatureC"]))


                w_year, w_month, w_date = month_date.split('-')
                monthinteger = int(w_month)
                month = datetime.date(1900, monthinteger, 1).strftime('%B')
                #print(month)
                final_date = month + " " + w_date + "  "
                #print(final_date)
                #print(month_date)
                date += {final_date}

            mintemp = row["Min TemperatureC"]
            if mintemp is not None and mintemp is not "":
                min_temp.append(float(row["Min TemperatureC"]))

            humidity = row["Max Humidity"]
            if humidity is not None and humidity is not "":
                hu_mid.append(float(row["Max Humidity"]))


    #print(date)
    #print(len(date))

    index, value = max(enumerate(max_temp), key=operator.itemgetter(1))
    print("Highest: ", value,"C on ", date[index])

    index, value = max(enumerate(min_temp), key=operator.itemgetter(1))
    print("Lowest: ", min(min_temp),"C on ", date[index])

    index, value = max(enumerate(hu_mid), key=operator.itemgetter(1))
    print("Humid: ", max(hu_mid),"% on ", date[index])
