import csv
from datetime import datetime


class WeathermanApplication:

    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def __init__(self, path):
        self.path = path
        self.weather_data_list = []
        
    def read_year_files(self, year):
        for i in range(12):
            try:
                filename = 'Murree_weather_{}_{}.txt'.format(year, self.MONTHS[i])
                with open(self.path + filename) as csvfile:
                    temp_list = []
                    reader = csv.DictReader(csvfile)
                    for day_weather in reader:
                        temp_list.append(day_weather)
                    self.weather_data_list.append(temp_list)
            except Exception as e :
                print("This Year doesnt exist or " + str(i) + " Month is not available")
                print(e)
        
    def read_month_files(self, year,month):
        try:
            filename = 'Murree_weather_{}_{}.txt'.format(year, self.MONTHS[month-1])
            with open(self.path + filename) as csvfile:
                temp_list = []
                reader = csv.DictReader(csvfile)
                for day_weather in reader:
                    temp_list.append(day_weather)
                self.weather_data_list.append(temp_list)
        except Exception as e :
            print("This Year doesnt exist or " + str(month) + " Month is not available")
            print(e)

    def find_highest_lowest_temperature_and_max_humidity(self):
        if len(self.weather_data_list) == 0:
            print("No data is available")
        max_tempC = max(int(day_weather["Max TemperatureC"]) if day_weather["Max TemperatureC"] != "" else 0 for day_weather in self.weather_data_list[0])
        max_tempC_date = datetime.now()
        for month in self.weather_data_list:
            for day_weather in month:
                temp = int(day_weather["Max TemperatureC"]) if day_weather["Max TemperatureC"] != "" else None
                if temp is not None and temp > max_tempC:
                    max_tempC_date = datetime.strptime(day_weather["PKT"], "%Y-%m-%d").date()
                    max_tempC = temp
        print("Maximum Temperature:",max_tempC,"C" , max_tempC_date.strftime("%b %d"))

        min_tempC = min(int(day_weather["Min TemperatureC"]) if day_weather["Min TemperatureC"] != "" else 0 for day_weather in self.weather_data_list[0])
        min_tempC_date = datetime.now()
        for month in self.weather_data_list:
            for day_weather in month:
                temp = int(day_weather["Min TemperatureC"]) if day_weather["Min TemperatureC"] != "" else None
                if temp is not None and temp < min_tempC:
                    min_tempC_date = datetime.strptime(day_weather["PKT"], "%Y-%m-%d").date()
                    min_tempC = temp
        print("Minimum Temperature:",min_tempC,"C" , min_tempC_date.strftime("%b %d"))

        max_humidity = max(int(day_weather["Max Humidity"]) if day_weather["Max Humidity"] != "" else 0 for day_weather in self.weather_data_list[0])
        max_humidity_date = datetime.now()
        for month in self.weather_data_list:
            for day_weather in month:
                temp = int(day_weather["Max Humidity"]) if day_weather["Max Humidity"] != "" else None
                if temp is not None and temp > max_humidity:
                    max_humidity_date = datetime.strptime(day_weather["PKT"], "%Y-%m-%d").date()
                    max_humidity = temp
        print("Maximum Humidity:",max_humidity,"%" , max_humidity_date.strftime("%b %d"))
        print()
    
    def find_average_max_temp_low_temp_and_mean_humidity(self):
        if len(self.weather_data_list) == 0:
            print("No data is available")
        day_counter = 0
        max_tempC_sum = 0
        for day_weather in self.weather_data_list[0]:
            if day_weather["Max TemperatureC"] != "":
                max_tempC_sum += int(day_weather["Max TemperatureC"])
                day_counter += 1
        avg_max_tempC = round(max_tempC_sum/day_counter,2)
        print("Average Highest:",avg_max_tempC,"C")

        day_counter = 0
        min_tempC_sum = 0
        for day_weather in self.weather_data_list[0]:
            if day_weather["Min TemperatureC"] != "":
                min_tempC_sum += int(day_weather["Min TemperatureC"])
                day_counter += 1
        avg_min_tempC = round(min_tempC_sum/day_counter,2)
        print("Average Lowest:",avg_min_tempC,"C")

        day_counter = 0
        mean_humidity_sum = 0
        for day_weather in self.weather_data_list[0]:
            if day_weather[" Mean Humidity"] != "":
                mean_humidity_sum += int(day_weather[" Mean Humidity"])
                day_counter += 1
        avg_mean_humidity = round(mean_humidity_sum/day_counter,2)
        print("Average Mean Humdidity:",avg_mean_humidity,"%")
        print()

    def bar_chart_vertically(self):
        if len(self.weather_data_list) == 0:
            print("No data is available")
        counter = 1
        for day_weather in self.weather_data_list[0]:
            max_temp = int(day_weather["Max TemperatureC"]) if day_weather["Max TemperatureC"] != "" else 0
            min_temp = int(day_weather["Min TemperatureC"]) if day_weather["Min TemperatureC"] != "" else 0
            print('\x1b[3;31m' + str(counter), abs(max_temp) * "+", max_temp, "C \x1b[0m")
            print('\x1b[3;34m' + str(counter), abs(min_temp) * "+", min_temp, "C \x1b[0m")
            counter += 1

    def bar_chart_horizentally(self):
        if len(self.weather_data_list) == 0:
            print("No data is available")
        counter = 1
        for day_weather in self.weather_data_list[0]:
            max_temp = int(day_weather["Max TemperatureC"]) if day_weather["Max TemperatureC"] != "" else 0
            min_temp = int(day_weather["Min TemperatureC"]) if day_weather["Min TemperatureC"] != "" else 0
            print('\x1b[3;34m' + str(counter), abs(min_temp) * "+" + '\x1b[3;31m', abs(max_temp) * "+", str(min_temp) + " - " + str(max_temp)+"C \x1b[0m")
            counter += 1
