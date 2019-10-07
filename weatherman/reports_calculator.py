from statistics import mean


def extract_year_records(weather_records, date):           
    return [record for record in weather_records if date.year == record.record_date.year]        


def extract_month_records(weather_records, date):   
    return [record for record in weather_records if date.year == record.record_date.year
            and date.month == record.record_date.month]  


def calculate_yearly_report(weather_records, year):
    year_records = extract_year_records(weather_records, year)

    if not year_records:
        return {}

    return {
        'max_temp_record': max(year_records, key=lambda record: record.max_temperature),
        'max_humidity_record': max(year_records, key=lambda record: record.max_humidity),
        'min_temp_record': min(year_records, key=lambda record: record.min_temperature)
    }
    

def calculate_monthly_report(weather_records, date):
    month_records = extract_month_records(weather_records, date)        
    if not month_records:
        return {} 

    return {
        'avg_max_temperature': round(mean([record.max_temperature for record in month_records]), 2),
        'avg_min_temperature': round(mean([record.min_temperature for record in month_records]), 2),
        'avg_mean_humidity': round(mean([record.mean_humidity for record in month_records]), 2)
    }
