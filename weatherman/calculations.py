import datetime
import statistics
import csv
import datetime
import glob
import Files_reading as reader

class Calculator:
    all_content = None
    max_temp = []
    min_temp = []
    max_humidity = []
    

    def converting_into_datetime(self, date):
        if date != '':
            date2 = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            return date2


    def calculating_averages(self, all_data, input_date):
        for row in all_data:
            if "PKST" in row.keys():
                date = self.converting_into_datetime(row["PKST"])
                if date != None:
                    if date.year == input_date.year and date.month == input_date.month:    
                        if  row["Max TemperatureC"] != '' :
                            self.max_temp.append(row["Max TemperatureC"])
                        if  row["Min TemperatureC"] != '' :
                            self.min_temp.append(row["Min TemperatureC"])
                        if  row[" Mean Humidity"] !='' :
                            self.max_humidity.append(row[" Mean Humidity"])
                                
            if "PKT" in row.keys():
                date = self.converting_into_datetime(row["PKT"])
                if date != None:
                    if date.year == input_date.year and date.month == input_date.month:    
                        if  row["Max TemperatureC"] != '':
                            self.max_temp.append(row["Max TemperatureC"])
                        if  row["Min TemperatureC"] != '':
                            self.min_temp.append(row["Min TemperatureC"])
                        if  row[" Mean Humidity"] != '':
                            self.max_humidity.append(row[" Mean Humidity"])
                            
        self.max_temp = [int(x) for x in self.max_temp if x]
        self.min_temp = [int(x) for x in self.min_temp if x]
        self.max_humidity = [int(x) for x in self.max_humidity if x]
        
        return max(self.max_temp), min(self.min_temp), max(self.max_humidity)


    def getting_temperatures(self, all_data, input_date):
        max_temp = []
        min_temp = []
        max_humidity = [] 
        for row in all_data:
            if "PKST" in row.keys():
                date=self.converting_into_datetime(row["PKST"])
                if date != None:
                    if date.year == input_date.year:    
                        if  row["Max TemperatureC"] != '':
                            max_temp.append ((row["PKST"], row["Max TemperatureC"]))
                        if  row["Min TemperatureC"] != '':    
                            min_temp.append ((row["PKST"], row["Min TemperatureC"]))
                        if  row["Max Humidity"] != '':    
                            max_humidity.append((row["PKST"], row["Max Humidity"]))
            
            if "PKT" in row.keys():
                date = self.converting_into_datetime(row["PKT"])
                if date != None:
                    if date.year == input_date.year:    
                        if  row["Max TemperatureC"] != '':
                            max_temp.append ((row["PKT"], row["Max TemperatureC"]))
                        if  row["Min TemperatureC"] != '':    
                            min_temp.append ((row["PKT"], row["Min TemperatureC"]))
                        if  row["Max Humidity"] !='' :    
                            max_humidity.append((row["PKT"], row["Max Humidity"]))
                    
        max_temp.sort(key = lambda x: int(x[1]))
        min_temp.sort(key = lambda x: int(x[1]))
        max_humidity.sort(key = lambda x: int(x[1]))
            
        return max_temp, min_temp, max_humidity
        

    def getting_min_max(self, all_data, input_date):
        final = []
        for row in all_data:
            if "PKST" in row.keys():
                date = self.converting_into_datetime(row["PKST"])
                if date != None:
                    if date.year == input_date.year and date.month == input_date.month:    
                        if  row["Max TemperatureC"] != '' and row["Min TemperatureC"] != '':
                            final.append ((row["PKST"], row["Max TemperatureC"],row["Min TemperatureC"]))

            if "PKT" in row.keys():
                date = self.converting_into_datetime(row["PKT"])
                if date != None:
                    if date.year == input_date.year and date.month == input_date.month:    
                       if  row["Max TemperatureC"] != '' and row["Min TemperatureC"] != '':
                            final.append ((row["PKT"], row["Max TemperatureC"],row["Min TemperatureC"]))
        
        return final
