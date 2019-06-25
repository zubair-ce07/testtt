import WeatherDataExtractor
import calendar


class ReportGenerator:
    def __init__(self, year, month, results):
        self.weather_data_obj = WeatherDataExtractor.WeatherDataExtractor(year, month)
        self.weather_data = self.weather_data_obj.read_all_files()
        self.results = results

    def year_report(self):
        high_temp, high_temp_day = self.results.highest_temp_in_year(self.weather_data)
        low_temp, low_temp_day = self.results.lowest_temp_in_year(self.weather_data)
        humidity, humid_day = self.results.most_humid_day_of_year(self.weather_data)
        print("Highest: "+str(high_temp)+"C on "+high_temp_day)
        print("Lowest: "+str(low_temp)+"C on "+low_temp_day)
        print("Humidity: "+str(humidity)+"% on "+humid_day)
        print("*******************************************")

    def month_report(self):
        high_temp = self.results.avg_highest_temp(self.weather_data)
        low_temp = self.results.avg_lowest_temp(self.weather_data)
        humidity = self.results.avg_mean_humidity(self.weather_data)
        print("Highest Average: "+str(high_temp)+"C")
        print("Lowest Average: "+str(low_temp)+"C")
        print("Average Mean Humidity: "+str(humidity)+"%")
        print("*******************************************")

    def draw_bar_charts(self):
        print(calendar.month_name[self.weather_data_obj.month]+" "+self.weather_data_obj.year)
        for i in self.weather_data:
            try:
                highest = "\033[0;34;50m" + ("+" * int(i.max_temperature))
                lowest = "\033[0;31;50m" + ("+" * int(i.min_temperature))
            except:
                continue
            if i.pkt[-2] == "-":
                print("\033[0;30;50m"+'0'+i.pkt[-1:]+" "+highest+"\033[0;30;50m"+i.max_temperature+"C")
                print("\033[0;30;50m"+'0'+i.pkt[-1:]+" "+lowest+"\033[0;30;50m"+i.min_temperature+"C")
            else:
                print("\033[0;30;m" + i.pkt[-2:]+" "+highest+"\033[0;30;m"+i.max_temperature+"C")
                print("\033[0;30;m" + i.pkt[-2:]+" "+lowest+"\033[0;30;m"+i.min_temperature+"C")
        print("*******************************************")

    def draw_single_chart(self):
        print(calendar.month_name[self.weather_data_obj.month]+" "+self.weather_data_obj.year)
        for i in self.weather_data:
            try:
                highest = "\033[0;34;50m"+"+" * int(i.max_temperature)
                lowest = "\033[0;31;50m"+"+" * int(i.min_temperature)
            except:
                continue
            if i.pkt[-2] == "-":
                print("\033[0;30;50m"+'0'+i.pkt[-1:]+" "+lowest+highest +
                      "\033[0;30;50m"+i.min_temperature+"C"+" "+i.max_temperature+"C")
            else:
                print(
                    "\033[0;30;50m"+i.pkt[-2:]+" "+lowest+highest +
                    "\033[0;30;50m"+i.min_temperature+"C"+" "+i.max_temperature+"C")
        print("*******************************************")
