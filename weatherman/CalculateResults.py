import calendar
import csv
import datetime
import glob

from temperatureResults import TempReading


class Results:

    def parse_files(self, path):
        temp_readings = []
        for temp_file_of_month in glob.glob(path + "/*"):
            temperature_file = open(temp_file_of_month)
            temperature_file_reader = csv.DictReader(temperature_file)
            temp_readings += [TempReading(datetime.datetime.strptime(day.get('PKT', day.get('PKST')), '%Y-%m-%d'),
                                          day['Max TemperatureC'],
                                          datetime.datetime.strptime(day.get('PKT', day.get('PKST')), '%Y-%m-%d'),
                                          day['Min TemperatureC'],
                                          datetime.datetime.strptime(day.get('PKT', day.get('PKST')), '%Y-%m-%d'),
                                          day['Max Humidity'],
                                          day[' Mean Humidity'])
                              for day in temperature_file_reader]
        return temp_readings

    def calculate_yearly_results(self, temp_readings, year):
        high_temperatures = [{"date": reading.date_high_temp, "temp": reading.high_temp} for reading in temp_readings if
                             reading.high_temp and
                             reading.date_high_temp.strftime('%Y') == year]
        highest_temperature = max(high_temperatures, key=lambda x: x["temp"])
        low_temperatures = [{"date": reading.date_low_temp, "temp": reading.low_temp} for reading in temp_readings if
                            reading.low_temp and
                            reading.date_low_temp.strftime('%Y') == year]
        lowest_temperature = min(low_temperatures, key=lambda x: x["temp"])
        humidity = [{"date": reading.date_humidity, "humidity": reading.humidity} for reading in temp_readings if
                    reading.humidity and
                    reading.date_humidity.strftime('%Y') == year]
        most_humid_day = max(humidity, key=lambda x: x["humidity"])
        result = TempReading(highest_temperature["date"], highest_temperature["temp"], lowest_temperature["date"],
                             lowest_temperature["temp"], most_humid_day["date"], most_humid_day["humidity"], 0)
        return result

    def calculate_avg(self, temp_readings, month):
        month_year = (int(month.split('/')[0]), int(month.split('/')[1]))
        total_days = calendar.monthrange(month_year[0], month_year[1])[1]
        avg_high_temperature = sum([reading.high_temp for reading in temp_readings if reading.high_temp and
                                    reading.date_high_temp.strftime('%Y/%m') == month]) / total_days
        avg_low_temperature = sum([reading.low_temp for reading in temp_readings if reading.low_temp and
                                   reading.date_low_temp.strftime('%Y/%m') == month]) / total_days
        avg_mean_humidity = sum([reading.mean_humidity for reading in temp_readings if reading.mean_humidity and
                                 reading.date_humidity.strftime('%Y/%m') == month]) / total_days
        averages_of_monthly_temp = \
            TempReading("", avg_high_temperature, "", avg_low_temperature, "", "", avg_mean_humidity)
        return averages_of_monthly_temp
