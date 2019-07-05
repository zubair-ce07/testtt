from ds import YearResults, MonthResults, ChartResults

def yearly_calc(year):
    max_temp = year.days[0].max_temp
    max_temp_date = year.days[0].date
    for temp_max_day in [day for day in year.days if day.max_temp]:
        if temp_max_day.max_temp > max_temp:
            max_temp = temp_max_day.max_temp
            max_temp_date = temp_max_day.date

    min_temp = year.days[0].min_temp
    min_temp_date = year.days[0].date
    for temp_min_day in [day for day in year.days if day.min_temp]:
        if temp_min_day.min_temp < min_temp:
            min_temp = temp_min_day.min_temp
            min_temp_date = temp_min_day.date

    max_humid = year.days[0].max_humidity
    max_humid_date = year.days[0].date
    for humid_max_day in [day for day in year.days if day.max_humidity]:
        if humid_max_day.max_humidity > max_humid:
            max_humid = humid_max_day.max_humidity
            max_humid_date = humid_max_day.date
    
    return YearResults(max_temp, max_temp_date, min_temp, min_temp_date, 
                       max_humid, max_humid_date, year.year)

def monthly_calc(month):
    high_temp_days = [day.max_temp for day in month.days if day.max_temp]
    avg_high_temp = round(sum(high_temp_days)/len(high_temp_days))

    low_temp_days = [day.min_temp for day in month.days if day.min_temp]
    avg_low_temp = round(sum(low_temp_days)/len(low_temp_days))

    mean_humid_days = [day.mean_humidity for day in month.days if day.mean_humidity]
    avg_mean_humid = round(sum(mean_humid_days)/len(mean_humid_days))

    return MonthResults(avg_high_temp, avg_low_temp, avg_mean_humid, 
                        month.month_name, month.year)

def bar_chart(month):
    results = []
    for day in [days for days in month.days if days.max_temp and days.min_temp]:
        results.append(tuple((day.date, day.max_temp, day.min_temp)))

    return ChartResults(results, month.month_name, month.year)
