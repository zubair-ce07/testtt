import datetime
import statistics
import datetime


class Calculator: 
    
    def converting_into_datetime(self, date):
        if date != '':
            date2 = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            return date2

    def calculating_averages(self, all_data, input_date):
        temperature_values = [record for record in all_data if self.is_valid(record, input_date)]         
        avg_max_temp = sum([item.max_temp for item in temperature_values])//len(temperature_values)
        avg_min_temp = sum([item.min_temp for item in temperature_values])//len(temperature_values)
        avg_mean_humidity = sum([item.max_humidity for item in temperature_values])//len(temperature_values)

        return avg_max_temp, avg_min_temp, avg_mean_humidity
        
    def getting_temperatures(self, all_data, input_date):
        temperature_values = [record for record in all_data if record.date.year == input_date.year]
        max_with_date = max(temperature_values, key=lambda item: item.max_temp)
        min_with_date = max(temperature_values, key=lambda item: item.min_temp)
        humd_with_date = max(temperature_values, key=lambda item: item.max_humidity) 
        
        return max_with_date, min_with_date, humd_with_date
        
    def getting_min_max(self, all_data, input_date):
        return [record for record in all_data if self.is_valid(record, input_date)]

    def is_valid(self, record, input_date):
        if record.date.year == input_date.year and record.date.month == input_date.month:
            return True
        else:
            return False 

