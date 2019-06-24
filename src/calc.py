from ds import YearResults, MonthResults, ChartResults

def yearly_calc(year):
    max_temp = year.months[0].days[0].max_temp
    max_temp_date = year.months[0].days[0].date
    for month in year.months:
        for temp_max_day in [day for day in month.days if day.max_temp]:
            if int(temp_max_day.max_temp) > int(max_temp):
                max_temp = temp_max_day.max_temp
                max_temp_date = temp_max_day.date

    min_temp = year.months[0].days[0].min_temp
    min_temp_date = year.months[0].days[0].date
    for month in year.months:
        for temp_min_day in [day for day in month.days if day.min_temp]:
            if int(temp_min_day.min_temp) < int(min_temp):
                min_temp = temp_min_day.min_temp
                min_temp_date = temp_min_day.date

    max_humid = year.months[0].days[0].max_humidity
    max_humid_date = year.months[0].days[0].date
    for month in year.months:
        for humid_max_day in [day for day in month.days if day.max_humidity]:
            if int(humid_max_day.max_humidity) > int(max_humid):
                max_humid = humid_max_day.max_humidity
                max_humid_date = humid_max_day.date
    
    return YearResults(max_temp, max_temp_date, min_temp, min_temp_date, max_humid, max_humid_date, year.year)

def monthly_calc(month):
    high_temp_days = [int(day.max_temp) for day in month.days if day.max_temp]
    sum_high_temp = sum(high_temp_days)
    avg_high_temp = round(sum_high_temp/len(high_temp_days))

    low_temp_days = [int(day.min_temp) for day in month.days if day.min_temp]
    sum_low_temp = sum(low_temp_days)
    avg_low_temp = round(sum_low_temp/len(low_temp_days))

    mean_humid_days = [int(day.mean_humidity) for day in month.days if day.mean_humidity]
    sum_mean_humid = sum(mean_humid_days)
    avg_mean_humid = round(sum_mean_humid/len(mean_humid_days))

    return MonthResults(avg_high_temp, avg_low_temp, avg_mean_humid, month.month_name, month.year)

def bar_chart(month):
    results = []
    days = [day for day in month.days if day.max_temp and day.min_temp]
    for day in days:
        day_data = tuple((day.date, int(day.max_temp), int(day.min_temp)))
        results.append(day_data)

    return ChartResults(results, month.month_name, month.year)
