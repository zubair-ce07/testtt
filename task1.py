import sys
import csv

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
filename = 'Murree_weather_'

option = 0
file_data = []
year_readings = []
csv_reader = []


class WeatherReading:
    def __init__(self, row):
        self.pkt = row[0]
        self.max_temp = row[1]
        self.mean_temp = row[2]
        self.min_temp = row[3]
        self.dew = row[4]
        self.mean_dew = row[5]
        self.min_dew = row[6]
        self.max_humidity = row[7]
        self.mean_humidity = row[8]
        self.min_humidity = row[9]
        self.max_sea_pressure = row[10]
        self.meam_sea_pressure = row[11]
        self.min_sea_pressure = row[12]
        self.max_visibility = row[13]
        self.mean_visibility = row[14]
        self.min_visibility = row[15]
        self.mean_windSpeed = row[17]
        self.max_gustSpeed = row[18]
        self.precipitation = row[19]
        self.cloudCover = row[20]
        self.events = row[21]
        self.win_dir_degrees = row[22]


class ParseFiles:
    def __init__(self, filename):

        self.monthreadings = []

        try:

            with open(filename, "r") as filestream:
                csv_reader = csv.reader(filestream)
                header = next(csv_reader)
                for row in csv_reader:
                    reading = WeatherReading(row)
                    if(row[header.index("Max TemperatureC")] != ''):
                        self.monthreadings.append(reading)

        except IOError:
            print("file does not exist")

    def __len__(self):
        length = 0
        for i in range(0, len(self.monthreadings)):
            length += 1
        return length

    def __getitem__(self, key):
        return self.monthreadings[key]


class Calculate_Month_Results:
    def __init__(self, monthreadings):
        self.high_average = 0
        self.low_average = 0
        self.mean_humidity_average = 0

        highsum = 0
        lowsum = 0
        humiditysum = 0

        for i in range(0, len(monthreadings)):
            highsum += (int(monthreadings[i].max_temp))
            lowsum += (int(monthreadings[i].min_temp))
            humiditysum += (int(monthreadings[i].mean_humidity))

        if(len(monthreadings) != 0):
            self.high_average = float(highsum / len(monthreadings))
            self.low_average = float(lowsum / len(monthreadings))
            self.mean_humidity_average = float(
                humiditysum / len(monthreadings))


class Print_Month_Averages:
    def __init__(self, month_data):
        print("Highest Average: " + str(month_data.high_average) + "C")
        print("Lowest Average: " + str(month_data.low_average) + "C")
        print("Average Mean Humidity: " +
              str(month_data.mean_humidity_average) + "%")
        print("---------------------------")


class Print_Month_Bar:
    def __init__(self, monthreadings):

        year, month, day = monthreadings[0].pkt.split("-")
        month = month_names[int(month) - 1]
        print(month, year)

        for i in range(0, len(monthreadings)):
            max = int(monthreadings[i].max_temp)
            min = int(monthreadings[i].min_temp)
            highnum = str(i + 1)
            lownum = str(i + 1)
            high = ' '
            low = ' '

            for j in range(0, max):
                high += "+"
            print(highnum + u"\u001b[31m" + str(high) + u"\u001b[0m" + " " +
                  str(max))

            for j in range(0, min):
                low += "+"
            print(lownum + u"\u001b[34m" + str(low) + u"\u001b[0m" + " " +
                  str(min))
        print("---------------------------")
        print(month, year)

        for i in range(0, len(monthreadings)):
            max = int(monthreadings[i].max_temp)
            min = int(monthreadings[i].min_temp)
            lownum = str(i + 1)
            high = ''
            low = ''

            for j in range(0, max):
                high += "+"
            for j in range(0, min):
                low += "+"
            print(lownum + u"\u001b[34m" + " " + str(low) + u"\u001b[0m" +
                  u"\u001b[31m" + str(high) + u"\u001b[0m"
                  + " " + str(min) + "C - " + str(max) + "C")

        print("---------------------------")


class Calculate_Year_Results:
    def __init__(self, year_readings):
        self.highest = int(year_readings[0][0].max_temp)
        self.lowest = int(year_readings[0][0].min_temp)
        self.humid = int(year_readings[0][0].max_humidity)
        self.highest_date = 0
        self.lowest_date = 0
        self.humid_date = 0

        for i in range(0, len(year_readings)):
            for j in range(0, len(year_readings[i])):
                if(int(year_readings[i][j].max_temp) > int(self.highest)):
                    self.highest = year_readings[i][j].max_temp
                    self.highest_date = year_readings[i][j].pkt

                if(int(year_readings[i][j].min_temp) < int(self.lowest)):
                    self.lowest = year_readings[i][j].min_temp
                    self.lowest_date = year_readings[i][j].pkt

                if(int(year_readings[i][j].max_humidity) > int(self.humid)):
                    self.humid = year_readings[i][j].max_humidity
                    self.humid_date = year_readings[i][j].pkt


class Print_Year_Results:
    def __init__(self, year_results):
        month_names = ['January', 'February', 'March', 'April', 'May',
                       'June', 'July', 'August', 'September', 'October',
                       'November', 'December']
        high_year, high_month, highest_day = year_results.highest_date.split(
            "-")
        lowest_year, lowest_month, lowest_day = year_results.lowest_date.split(
            "-")
        humid_year, humid_month, humid_day = year_results.humid_date.split("-")

        high_temp_month = month_names[int(high_month) - 1]
        lowest_temp_month = month_names[int(lowest_month) - 1]
        most_humid_month = month_names[int(humid_month) - 1]

        print("Highest: " + str(year_results.highest) + "C on " +
              str(high_temp_month) + " " + highest_day)
        print("Lowest: " + str(year_results.lowest) + "C on " +
              str(lowest_temp_month) + " " + lowest_day)
        print("Most Humidity: " + str(year_results.humid) +
              '% on' + str(most_humid_month) + " " + humid_day)
        print("---------------------------")


def main():

    for i in range(2, len(sys.argv[1:]) + 1):

        word = sys.argv[i]

        if(word == '-a'):
            option = 1
        if(word == '-c'):
            option = 2
        if(word == '-e'):
            option = 3

        if("/" in word):
            year, month = word.split("/")
            filename = 'Murree_weather_'
            filename += (year + "_" + month_names[int(month) - 1] + ".txt")
            filename = sys.argv[1] + "/" + filename

            file_data = (ParseFiles(filename))
            if(option == 1):
                month_results = Calculate_Month_Results(file_data)
                Print_Month_Averages(month_results)

            elif(option == 2):
                Print_Month_Bar(file_data.monthreadings)

        elif(len(word) > 2):
            for j in range(0, 12):
                filename = 'Murree_weather_'
                filename += (word + "_" + month_names[j] + ".txt")
                filename = sys.argv[1] + "/" + filename

                file_data = (ParseFiles(filename))
                year_readings.append(file_data.monthreadings)

            year_results = Calculate_Year_Results(year_readings)
            Print_Year_Results(year_results)


if __name__ == "__main__":
    main()
