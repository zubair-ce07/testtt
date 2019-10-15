from operator import itemgetter


class monthly_computing_results:
    """
    This class takes the objects from list and computing monthly results
    """

    def getting_monthly_objects(self,record,year,month):
        calculating_records = []
        for index in range(len(record)):
            for key in record[index]:        
                if(record[index][key].startswith(year + '-' + month)):
                    calculating_records.append(record[index])
        return calculating_records

    def getmaximumaverage(self,req_objects):
        row_count = sum(1 for row in req_objects)
        max_temperature = [ sub['Max TemperatureC'] for sub in req_objects]
        convert_list = list(map(int, max_temperature))
        sum_of_max_temperature = sum(convert_list)
        average = int(sum_of_max_temperature) / row_count
        print("Maximum Average Temperature:", int(average), "C")

    def getminimumaverage(self,req_objects):
        row_count = sum(1 for row in req_objects)
        min_temperature = [ sub['Min TemperatureC'] for sub in req_objects]
        convert_list = list(map(int, min_temperature))
        sum_of_min_temperature = sum(convert_list)
        average = int(sum_of_min_temperature) / row_count
        print("Minimum Average Temperature:", int(average), "C")

    def gethumidityaverage(self,req_objects):
        row_count = sum(1 for row in req_objects)
        mean_humidty = [ sub[' Mean Humidity'] for sub in req_objects]
        convert_list = list(map(int, mean_humidty))
        sum_of_mean_humidity = sum(convert_list)
        average = int(sum_of_mean_humidity) / row_count
        print("Mean Humidity Average:", int(average), "%")


class yearly_computing_results:
    """
    This class takes the objects from list and computing yearly results
    """


    def getting_yearly_objects(self,record,year):
        calculating_records = []
        for index in range(len(record)):
            for key in record[index]:        
                if(record[index][key].startswith(year)):
                    calculating_records.append(record[index])

        return calculating_records

    def gethighesttemperature(self,req_objects):
        max_temperature = [ sub['Max TemperatureC'] for sub in req_objects]
        max_temp = list(map(int, max_temperature))
        pkt = [ sub['PKT'] for sub in req_objects] or [ sub['PKST'] for sub in req_objects]
        merge = list(zip(max_temp,pkt))
        result = max(merge,key=itemgetter(0))
        print("Highest Temperature And Day: ", result)

    def getlowesttemperature(self,req_objects):
        min_temperature = [ sub['Min TemperatureC'] for sub in req_objects]
        min_temp = list(map(int, min_temperature))
        pkt = [ sub['PKT'] for sub in req_objects] or [ sub['PKST'] for sub in req_objects]
        merge = list(zip(min_temp,pkt))
        result = min(merge,key=itemgetter(0))
        print("Lowest Temperature And Day: ", result)

    def gethighesthumidity(self,req_objects):
        max_humidity = [ sub['Max Humidity'] for sub in req_objects]
        max_humid = list(map(int, max_humidity))
        pkt = [ sub['PKT'] for sub in req_objects] or [ sub['PKST'] for sub in req_objects]
        merge = list(zip(max_humid,pkt))
        result = min(merge,key=itemgetter(0))
        print("Max Humidity And Day: ", result)
