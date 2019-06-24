import ResultStorage
import calendar

class ReportGenerator:

# generate report for a year
    def yearReport(self,resultObj):
        print("Highest: ",resultObj.highestTemp, "C on ", resultObj.highestTempDay )
        print("Lowest: ", resultObj.lowestTemp, "C on ", resultObj.lowestTempDay)
        print("Humidity: ", resultObj.humidity, "% on ", resultObj.humidityDay)
        print("*******************************************")

# generate report for a month
    def monthReport(self,resultObj):
        print("Highest Average: ",resultObj.highestTemp, "C")
        print("Lowest Average: ", resultObj.lowestTemp, "C")
        print("Average Mean Humidity: ", resultObj.humidity, "%")
        print("*******************************************")

# draw seperate bar chart for highest and lowest temperature
    def drawBarCharts(self, requiredDays, allDataArray, month, year):
        try:
            print(calendar.month_name[int(month)] , year)  # print month and year
        except:
            print("Invalid Month")
            return
        for i in requiredDays:
            try:
                highest = "\033[0;34;50m" + ("+" * int(allDataArray[i].maxTemperature))
                lowest = "\033[0;31;50m" + ("+" * int(allDataArray[i].minTemperature))
            except:
                continue
            if (allDataArray[i].pkt[-2] == "-"): #printing colored bar chart on terminal
                print("\033[0;30;50m" +'0'+allDataArray[i].pkt[-1:], " ", highest, "\033[0;30;50m" + allDataArray[i].maxTemperature, "C")
                print("\033[0;30;50m" +'0'+allDataArray[i].pkt[-1:], " ", lowest, "\033[0;30;50m" + allDataArray[i].minTemperature, "C")
            else:
                print("\033[0;30;m" +allDataArray[i].pkt[-2:], " ", highest, "\033[0;30;m" + allDataArray[i].maxTemperature, "C")
                print("\033[0;30;m" +allDataArray[i].pkt[-2:], " ", lowest, "\033[0;30;m" + allDataArray[i].minTemperature, "C")
        print("*******************************************")

# draw single bar chart on terminal
    def drawSingleChart(self,requiredDays, allDataArray,month,year):
        try:
            print(calendar.month_name[int(month)] , year)
        except:
            print("Invalid Month")
            return
        for i in requiredDays:
            try:
                highest = "\033[0;34;50m" + "+" * int(allDataArray[i].maxTemperature)
                lowest = "\033[0;31;50m" + "+" * int(allDataArray[i].minTemperature)
            except:
                continue
            if (allDataArray[i].pkt[-2] == "-"):
                print("\033[0;30;50m" +'0'+allDataArray[i].pkt[-1:], " ", lowest, highest, "\033[0;30;50m" + allDataArray[i].minTemperature, "C" + " ", allDataArray[i].maxTemperature, "C")
            else:
                print("\033[0;30;50m" + allDataArray[i].pkt[-2:], " ", lowest + highest, "\033[0;30;50m"  + allDataArray[i].minTemperature, "C" + " " , allDataArray[i].maxTemperature, "C")
        print("*******************************************")

