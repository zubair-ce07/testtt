import sys
import helper.common as common
from model.temperaturerange import TemperatureRange
from model.tempchart import TempChart
from model.avgtemp import AvgTemp


class WeatherMan:


    def temperature_range(self, Date, CSVData):

        TempRange = TemperatureRange()
        StatsData = TempRange.stats(Date, CSVData)
        
        if (StatsData['highest']['temp'] and StatsData['highest']['date']):
            print ("Highest: ", StatsData['highest']['temp'], "C on ", common.format_date(StatsData['highest']['date']))
        else:
            print ("No Data exist for Highest temperature")
        
        if (StatsData['lowest']['temp'] and StatsData['lowest']['date']):
            print ("Lowest: ", StatsData['lowest']['temp'], "C on ", common.format_date(StatsData['lowest']['date']))
        else:
            print ("No Data exist for Lowest temperature")
        
        if (StatsData['humid']['humidity'] and StatsData['humid']['date']):
            print ("Humid: ", StatsData['humid']['humidity'], "% on ", common.format_date(StatsData['humid']['date']))
        else:
            print ("No Data exist for Humidity")
        
        
    
    def avg_temp(self, Date, CSVData):
        
        Temp = AvgTemp()
        StatsData = Temp.stats(Date, CSVData)
    
        if (StatsData['highest']['avg'] and StatsData['highest']['avg']):
            print ("Highest Average: ", StatsData['highest']['avg'], "C")
        else:
            print ("Highest Average: No Data Exists")
        
        if (StatsData['lowest']['avg'] and StatsData['lowest']['avg']):
            print ("Lowest Average: ", StatsData['lowest']['avg'], "C")
        else:
            print ("Lowest Average: No Data Exists")
        
        if (StatsData['humidity']['avg'] and StatsData['humidity']['avg']):
            print ("Average Humidity: ", StatsData['humidity']['avg'], "%")
        else:
            print ("Average Humidity: No Data Exists")
        

    def temp_chart(self, Date, CSVData):
        
        Chart = TempChart()
        StatsData = Chart.stats(Date, CSVData)
        
        if (len(StatsData) > 0):
            for Row in StatsData:
                print (Row) 
        else:
            print ("No Data Exists.")



    def draw_multiple_bars(self, Date, CSVData):

        Chart = TempChart()
        StatsData = Chart.combine_stats(Date, CSVData)
        if (len(StatsData) > 0):
            for Row in StatsData:
                print (Row)
        else:
            print ("No Data Exists.")

