import calendar
import csv


class FilesParser:

    def populate_yearly_temps(self, highest_temp_yearly_days, lowest_temp_yearly_days, highest_humid_yearly_days, path,
                              year):
        for i in range(1, 13):
            month = calendar.month_abbr[int(i)]
            temp_path = path + "/Murree_weather_" + year + "_" + month + ".txt"
            try:
                csv_file = open(temp_path)
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for day in csv_reader:
                    if day['Max TemperatureC'] != "":
                        highest_temp_yearly_days[day.get('PKT',day.get('PKST'))] = int(day['Max TemperatureC'])
                    if day['Min TemperatureC'] != "":
                        lowest_temp_yearly_days[day.get('PKT',day.get('PKST'))] = int(day['Min TemperatureC'])
                    if day['Max Humidity'] != "":
                        highest_humid_yearly_days[day.get('PKT',day.get('PKST'))] = int(day['Max Humidity'])
            except:
                continue

    def populate_monthly_avgs(self, highest_mnthly_for_avg, lowest_mnthly_for_avg, mean_humidity_monthly_days,
                              path, month):
        month_n = month.split('/')[1]
        temp_path = path + "/Murree_weather_" + month.split('/')[0] + "_" + calendar.month_abbr[int(month_n)] + ".txt"
        csv_file = open(temp_path)
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for day in csv_reader:
            if day['Max TemperatureC'] != "":
                highest_mnthly_for_avg[day.get('PKT',day.get('PKST'))] = int(day['Max TemperatureC'])
            if day['Min TemperatureC'] != "":
                lowest_mnthly_for_avg[day.get('PKT',day.get('PKST'))] = int(day['Min TemperatureC'])
            if day[' Mean Humidity'] != "":
                mean_humidity_monthly_days[day.get('PKT',day.get('PKST'))] = int(day[' Mean Humidity'])
