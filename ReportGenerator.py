import ResultStorage, CalculationsResults

class ReportGenerator:

    def yearReport(self,resultObj):
        print("Highest: ",resultObj.highestTemp, "C on ", resultObj.highestTempDay )
        print("Lowest: ", resultObj.lowestTemp, "C on ", resultObj.lowestTempDay)
        print("Humidity: ", resultObj.humidity, "% on ", resultObj.humidityDay)
        print("*******************************************")


    def monthReport(self,resultObj):
        print("Highest Average: ",resultObj.highestTemp, "C")
        print("Lowest Average: ", resultObj.lowestTemp, "C")
        print("Average Mean Humidity: ", resultObj.humidity, "%")
        print("*******************************************")


    def drawBarCharts(self, requiredDays, allDataArray):
        for i in requiredDays:
            highest = "\033[0;34;50m" + "+" * int(allDataArray[i].maxTemperature)
            lowest = "\033[0;31;50m" + "+" * int(allDataArray[i].minTemperature)
            if (allDataArray[i].pkt[-2] == "-"):
                print("\033[0;30;50m" +'0'+allDataArray[i].pkt[-1:], " ", highest, "\033[0;30;50m" + allDataArray[i].maxTemperature, "C")
                print("\033[0;30;50m" +'0'+allDataArray[i].pkt[-1:], " ", lowest, "\033[0;30;50m" + allDataArray[i].minTemperature, "C")
            else:
                print("\033[0;30;m" +allDataArray[i].pkt[-2:], " ", highest, "\033[0;30;m" + allDataArray[i].maxTemperature, "C")
                print("\033[0;30;m" +allDataArray[i].pkt[-2:], " ", lowest, "\033[0;30;m" + allDataArray[i].minTemperature, "C")


    def drawSingleChart(self,requiredDays, allDataArray):
        for i in requiredDays:
            highest = "\033[0;34;50m" + "+" * int(allDataArray[i].maxTemperature)
            lowest = "\033[0;31;50m" + "+" * int(allDataArray[i].minTemperature)
            if (allDataArray[i].pkt[-2] == "-"):
                print("\033[0;30;50m" +'0'+allDataArray[i].pkt[-1:], " ", lowest, highest, "\033[0;30;50m" + allDataArray[i].minTemperature, "C" + " ", allDataArray[i].maxTemperature, "C")
            else:
                print("\033[0;30;50m" + allDataArray[i].pkt[-2:], " ", lowest + highest, "\033[0;30;50m"  + allDataArray[i].minTemperature, "C" + " " , allDataArray[i].maxTemperature, "C")


