import datetime

class Calculations:

    @staticmethod
    def calulate_year_wise_record(weather_readings):

        highest_temp_record = max(weather_readings, key=lambda x:x["Max TemperatureC"])
        lowest_temp_record = min(weather_readings, key=lambda x:x["Min TemperatureC"])
        max_humidity_record = max(weather_readings, key=lambda x:x["Max Humidity"])

        results = {"Highest Temperature":highest_temp_record,
                    "Lowest Temperature":lowest_temp_record,
                    "Max Humidity":max_humidity_record}
       
        return results

    @staticmethod
    def calulate_average_record(weather_readings):
        highest_temperature_list = []
        lowest_temperature_list = []
        mean_humidity_list = []
        
        for reading in weather_readings:
            if reading.get("Max TemperatureC") or reading.get(" Max TemperatureC"):
                highest_temperature_list.append(int(reading.get("Max TemperatureC") or reading.get(" Max TemperatureC")))
        
        for reading in weather_readings:
            if reading.get("Min TemperatureC") or reading.get(" Min TemperatureC"):
                lowest_temperature_list.append(int(reading.get("Min TemperatureC") or reading.get(" Min TemperatureC")))
        
        for reading in weather_readings:
            if reading.get("Mean Humidity") or reading.get(" Mean Humidity"):
                mean_humidity_list.append(int(reading.get("Mean Humidity") or reading.get(" Mean Humidity")))
        
        results = {"Highest Average":sum(highest_temperature_list) / len(highest_temperature_list),
                    "Lowest Average":sum(lowest_temperature_list) / len(lowest_temperature_list),
                    "Average Mean Humidity":sum(mean_humidity_list) / len(mean_humidity_list)}
        
        return results
