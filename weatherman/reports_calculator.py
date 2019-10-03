from statistics import mean


def calculate_yearly_report(year_records):    
                         
    return {
        'max_temp_record': max(year_records, key=lambda record: record.max_temperature),
        'max_humidity_record': max(year_records, key=lambda record: record.max_humidity),
        'min_temp_record': min(year_records, key=lambda record: record.min_temperature)
    } if year_records else {}
    

def calculate_monthly_report(month_records):        
           
    return {
        'avg_max_temperature': round(mean([record.max_temperature for record in month_records]), 2),
        'avg_min_temperature': round(mean([record.min_temperature for record in month_records]), 2),
        'avg_mean_humidity': round(mean([record.mean_humidity for record in month_records]), 2)
    } if month_records else {}
   