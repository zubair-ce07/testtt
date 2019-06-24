import ResultStorage
import calendar
import WeatherDataExtractor
import calendar


class ReportGenerator:
    def __init__(self, year, month,results):
        self.weather_data_obj = WeatherDataExtractor.WeatherDataExtractor(year, month)
        self.weatherData = self.weather_data_obj.read_all_files()
        self.results = results


# generate report for a year
    def yearReport(self):
        high_temp, high_temp_day = self.results.highestTempInYear(self.weatherData)
        low_temp, low_temp_day = self.results.lowestTempInYear(self.weatherData)
        humidity, humid_day = self.results.mostHumidDayOfYear(self.weatherData)
        print("Highest: "+ str(high_temp)+ "C on "+ high_temp_day)
        print("Lowest: "+ str(low_temp)+ "C on "+ low_temp_day)
        print("Humidity: "+str(humidity)+ "% on "+humid_day)
        print("*******************************************")

# generate report for a month
    def monthReport(self):
        high_temp = self.results.avgHighestTemp(self.weatherData)
        low_temp = self.results.avgLowestTemp(self.weatherData)
        humidity = self.results.avgMeanHumidity(self.weatherData)
        print("Highest Average: "+str(high_temp)+"C")
        print("Lowest Average: "+str(low_temp)+"C")
        print("Average Mean Humidity: "+str(humidity)+ "%")
        print("*******************************************")

# draw seperate bar chart for highest and lowest temperature
    def drawBarCharts(self):
        print(calendar.month_name[self.weather_data_obj.month]+" "+self.weather_data_obj.year)
        for i in self.weatherData:
            try:
                highest = "\033[0;34;50m" + ("+" * int(i.maxTemperature))
                lowest = "\033[0;31;50m" + ("+" * int(i.minTemperature))
            except:
                continue
            if (i.pkt[-2] == "-"): #printing colored bar chart on terminal
                print("\033[0;30;50m" +'0'+ i.pkt[-1:]+ " "+ highest+ "\033[0;30;50m" + i.maxTemperature+ "C")
                print("\033[0;30;50m" +'0'+ i.pkt[-1:]+ " "+ lowest+ "\033[0;30;50m" + i.minTemperature+ "C")
            else:
                print("\033[0;30;m" + i.pkt[-2:]+ " "+ highest+ "\033[0;30;m" + i.maxTemperature+ "C")
                print("\033[0;30;m" + i.pkt[-2:]+ " "+ lowest+ "\033[0;30;m" + i.minTemperature+ "C")
        print("*******************************************")

# draw single bar chart on terminal
    def drawSingleChart(self):
        print(calendar.month_name[self.weather_data_obj.month]+" "+self.weather_data_obj.year)
        for i in self.weatherData:
            try:
                highest ="\033[0;34;50m" + "+" * int(i.maxTemperature)
                lowest = "\033[0;31;50m" + "+" * int(i.minTemperature)
            except:
                continue
            if (i.pkt[-2] == "-"):
                print("\033[0;30;50m" +'0'+i.pkt[-1:]+ " "+ lowest+ highest+ "\033[0;30;50m" + i.minTemperature+ "C" + " "+ i.maxTemperature+ "C")
            else:
                print("\033[0;30;50m" + i.pkt[-2:]+ " "+ lowest + highest+ "\033[0;30;50m"  + i.minTemperature+ "C" + " " + i.maxTemperature+ "C")
        print("*******************************************")

