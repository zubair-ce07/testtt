from ds import YearResults, MonthResults, ChartResults

def yearly_calc(year):
    max_temp = year.months[0].days[0].max_temp
    max_temp_date = year.months[0].days[0].date
    for month in year.months:
        temp_max_days = [day for day in month.days if day.max_temp]
        for day in temp_max_days:
            if int(day.max_temp) > int(max_temp):
                max_temp = day.max_temp
                max_temp_date = day.date

    min_temp = year.months[0].days[0].min_temp
    min_temp_date = year.months[0].days[0].date
    for month in year.months:
        temp_min_days = [day for day in month.days if day.min_temp]
        for day in temp_min_days:
            if int(day.min_temp) < int(min_temp):
                min_temp = day.min_temp
                min_temp_date = day.date

    max_humid = year.months[0].days[0].max_humidity
    max_humid_date = year.months[0].days[0].date
    for month in year.months:
        humid_max_days = [day for day in month.days if day.max_humidity]
        for day in humid_max_days:
            if int(day.max_humidity) > int(max_humid):
                max_humid = day.max_humidity
                max_humid_date = day.date
    
    return YearResults(max_temp, max_temp_date, min_temp, min_temp_date, max_humid, max_humid_date)

def monthly_calc(month):
    sum_high_t = 0
    high_temp_days = [day for day in month.days if day.max_temp]
    for day in high_temp_days:
        sum_high_t = sum_high_t + int(day.max_temp)
    avg_high_t = round(sum_high_t/len(high_temp_days))

    sum_low_t = 0
    low_temp_days = [day for day in month.days if day.min_temp]
    for day in low_temp_days:
        sum_low_t = sum_low_t + int(day.min_temp)
    avg_low_t = round(sum_low_t/len(low_temp_days))

    sum_mean_h = 0
    mean_humid_days = [day for day in month.days if day.mean_humidity]
    for day in mean_humid_days:
        sum_mean_h = sum_mean_h + int(day.mean_humidity)
    avg_mean_h = round(sum_mean_h/len(mean_humid_days))

    return MonthResults(avg_high_t, avg_low_t, avg_mean_h)

def bar_chart(month):
    high_t = []
    high_d = []
    high_temp_days = [day for day in month.days if day.max_temp]
    for day in high_temp_days:
        high_t.append(day.max_temp)
        high_d.append(day.date)
    
    low_t = []
    low_d = []
    low_temp_days = [day for day in month.days if day.min_temp]
    for day in low_temp_days:
        low_t.append(day.min_temp)
        low_d.append(day.date)

    return ChartResults(high_t, low_t, high_d, low_d, month.month_name, month.year)
