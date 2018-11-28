import calendar
import csv
import glob


def file_reading(dir_path, year, month):

    if month:
        files = glob.glob(dir_path + "/*_weather_" + year + "_" +
                          calendar.month_abbr[int(month)] + "*")
    else:
        files = glob.glob(dir_path + "/*_weather_" + year + "_" + "*")

    if files:
        weather_data = []
        for file in files:
            file_reader = open(file)
            csv_reader = csv.DictReader(file_reader)

            if csv_reader:
                for dict_row in csv_reader:
                    weather_data.append(dict(dict_row))

        return weather_data
    else:
        print("Data not found")
