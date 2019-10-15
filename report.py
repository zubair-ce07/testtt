class monthly_report:
    """
    This class takes the objects from list and draw multiline chart on console
    """


    def getting_monthly_objects(self,record,year,month):
        calculating_records = []
        for index in range(len(record)):
            for key in record[index]:        
                if(record[index][key].startswith(year + '-' + month)):
                    calculating_records.append(record[index])

        return calculating_records
    
    def monthly_chart(self,req_objects):

        COLOR_BLUE = '\033[1;34;48m'
        COLOR_RED = '\033[1;31;48m'
        
        max_temperature = [ sub['Max TemperatureC'] for sub in req_objects]
        max_temp_convert_list = list(map(int, max_temperature))
        min_temperature = [ sub['Min TemperatureC'] for sub in req_objects]
        min_temp_convert_list = list(map(int, min_temperature))
        pkt = [ sub['PKT'] for sub in req_objects] or [ sub['PKST'] for sub in req_objects]

        for pkt,max_temp,min_temp in zip(pkt,max_temp_convert_list,min_temp_convert_list):
            print(f"{pkt}{COLOR_RED.format('+' * max_temp)}{max_temp}C")
            print(f"{pkt}{COLOR_BLUE.format('+' * min_temp)}{min_temp}C")

                    
class monthly_bonus_report:
    """
    This class takes the objects from list and draw single line chart on console
    """
    

    def getting_monthly_objects(self,record,year,month):
        calculating_records = []
        for index in range(len(record)):
            for key in record[index]:        
                if(record[index][key].startswith(year + '-' + month)):
                    calculating_records.append(record[index])

        return calculating_records
    
    def bonus_chart(self,req_objects):
        COLOR_BLUE = '\033[1;34;48m'
        COLOR_RED = '\033[1;31;48m'
        
        max_temperature = [ sub['Max TemperatureC'] for sub in req_objects]
        max_temp_convert_list = list(map(int, max_temperature))
        min_temperature = [ sub['Min TemperatureC'] for sub in req_objects]
        min_temp_convert_list = list(map(int, min_temperature))
        pkt = [ sub['PKT'] for sub in req_objects] or [ sub['PKST'] for sub in req_objects]

        for pkt,max_temp,min_temp in zip(pkt,max_temp_convert_list,min_temp_convert_list):
            print(f"{pkt}{COLOR_RED.format('+' * max_temp)}"
            f"{COLOR_BLUE.format('+' * min_temp)}{max_temp}C-{min_temp}C")
