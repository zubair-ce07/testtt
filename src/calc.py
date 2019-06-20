from ds import YearResults
from ds import MonthResults
from ds import ChartResults

def yearlyCalc(year):
    max_t = year.months[0].days[0].max_temp
    max_t_date = year.months[0].days[0].date
    for month in year.months:
        for day in month.days:
            if (day.max_temp == ''):
                continue
            if (int(day.max_temp) > int(max_t)):
                max_t = day.max_temp
                max_t_date = day.date

    min_t = year.months[0].days[0].min_temp
    min_t_date = year.months[0].days[0].date
    for month in year.months:
        for day in month.days:
            if (day.min_temp == ''):
                continue
            if (int(day.min_temp) < int(min_t)):
                min_t = day.min_temp
                min_t_date = day.date

    max_h = year.months[0].days[0].max_humidity
    max_h_date = year.months[0].days[0].date
    for month in year.months:
        for day in month.days:
            if (day.max_humidity == ''):
                continue
            if (int(day.max_humidity) > int(max_h)):
                max_h = day.max_humidity
                max_h_date = day.date
    year_res = YearResults(max_t, max_t_date, min_t, min_t_date, max_h, max_h_date)
    return year_res

def monthlyCalc(month):
    sum_high_t = 0
    count_high_t = 0
    for day in month.days:
        if (day.max_temp == ''):
            continue
        sum_high_t = sum_high_t + int(day.max_temp)
        count_high_t += 1
    avg_high_t = sum_high_t/count_high_t
    avg_high_t = round(avg_high_t)

    sum_low_t = 0
    count_low_t = 0
    for day in month.days:
        if (day.min_temp == ''):
            continue
        sum_low_t = sum_low_t + int(day.min_temp)
        count_low_t += 1
    avg_low_t = sum_low_t/count_low_t
    avg_low_t = round(avg_low_t)

    sum_mean_h = 0
    count_mean_h = 0
    for day in month.days:
        if (day.mean_humidity == ''):
            continue
        sum_mean_h = sum_mean_h + int(day.mean_humidity)
        count_mean_h += 1
    avg_mean_h = sum_mean_h/count_mean_h
    avg_mean_h = round(avg_mean_h)

    month_res = MonthResults(avg_high_t, avg_low_t, avg_mean_h)
    return month_res

def barChart(month):
    high_t = []
    high_d = []
    for day in month.days:
        if (day.max_temp == ''):
            continue
        high_t.append(day.max_temp)
        high_d.append(day.date)
    
    low_t = []
    low_d = []
    for day in month.days:
        if (day.min_temp == ''):
            continue
        low_t.append(day.min_temp)
        low_d.append(day.date)

    chart_res = ChartResults(high_t, low_t, high_d, low_d, month.month_name, month.year)
    return chart_res
