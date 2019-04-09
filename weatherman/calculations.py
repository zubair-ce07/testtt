import datetime

class Calculator: 
    
    def calculating_averages(self, all_data, input_date):
        records = [record for record in all_data if self.is_valid(record, input_date)]         
        avg_max_temp = sum([item.max_temp for item in records]) // len(records)
        avg_min_temp = sum([item.min_temp for item in records]) // len(records)
        avg_mean_humidity = sum([item.max_humidity for item in records]) // len(records)

        return avg_max_temp, avg_min_temp, avg_mean_humidity
        
    def getting_temperatures(self, all_data, input_date):
        records = [record for record in all_data if record.date.year == input_date.year]
        record_max_temp = max(records, key=lambda item: item.max_temp)
        record_min_temp = max(records, key=lambda item: item.min_temp)
        record_max_humd = max(records, key=lambda item: item.max_humidity) 
        
        return record_max_temp, record_min_temp, record_max_humd
        
    def getting_min_max(self, all_data, input_date):
        return [record for record in all_data if self.is_valid(record, input_date)]

    def is_valid(self, record, input_date):
        return record.date.year == input_date.year and record.date.month == input_date.month

