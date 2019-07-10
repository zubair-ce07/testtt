import math
import statistics


def weather_calculations(years, months, data):
    """This function will perform all the calculations on the weather data"""


    all_years_data = []

    for y in years:
        yearly = [y]

        for m in months:

            if y + '_' + m in data.keys():
                monthly = [m]
                

                max_temps = data[y + '_' + m]['Max TemperatureC']

                max_temp_month = max(
                    x for x in max_temps if x is not None)
                
                avg_max_temp = statistics.mean(
                    x for x in max_temps if x is not None)
                
                max_temp_day = max_temps.index(max_temp_month) + 1
                max_temps = [-math.inf if x is None else x for x in max_temps]
                

                monthly.append(max_temp_month)
                monthly.append(avg_max_temp)
                monthly.append(max_temp_day)
                monthly.append(max_temps)


                min_temps = data[y + '_' + m]['Min TemperatureC']
                
                min_temp_month = min(
                    x for x in min_temps if x is not None)
                
                avg_min_temp = statistics.mean(
                    x for x in min_temps if x is not None)
                
                min_temp_day = min_temps.index(min_temp_month) + 1
                
                min_temps = [math.inf if x is None else x for x in min_temps]
                

                monthly.append(min_temp_month)
                monthly.append(avg_min_temp)
                monthly.append(min_temp_day)
                monthly.append(min_temps)


                max_humids = data[y + '_' + m]['Max Humidity']
                
                max_humid_month = max(
                    x for x in max_humids if x is not None)
                
                max_humid_day = max_humids.index(max_humid_month) + 1
                

                monthly.append(max_humid_month)
                monthly.append(max_humid_day)
                

                mean_humids = data[y + '_' + m][' Mean Humidity']
                avg_mean_humid = statistics.mean(x for x in mean_humids if x is not None)
                

                monthly.append(avg_mean_humid)
                
                
                yearly.append(monthly)

        all_years_data.append(yearly)
    return all_years_data


def calculate_yearly(years, months, years_monthly_records):
    """This calculates yearly maximums and minimums."""


    yearly_record = {}

    for y in years:
        
        for an_year in years_monthly_records:
            if an_year[0] == y:

                max_temp = -math.inf
                max_humid = -math.inf
                min_temp = math.inf
                max_temp_day = -1
                max_humid_day = -1
                min_temp_day = -1
                
                for each_month in an_year[1:]:
                    if each_month[1] > max_temp:
                
                        max_temp = each_month[1]
                        max_temp_day = each_month[0] + ' ' + str(each_month[3])
                    elif each_month[9] > max_humid:
                
                        max_humid = each_month[9]
                        max_humid_day = each_month[0] + ' ' + str(each_month[10])
                    elif each_month[5] < min_temp:
                
                        min_temp = each_month[5]
                        min_temp_day = each_month[0] + ' ' + str(each_month[7])
                yearly_record[y] = {
                    "Highest: ": str(max_temp) + 'C ' + max_temp_day,
                    "Lowest: ": str(min_temp) + 'C ' + min_temp_day,
                    "Humidity: ": str(max_humid) + "% " + max_humid_day
                    }
    return yearly_record
