from yearly_temp import YearlyTempResultData
from monthlyAvgs import MonthlyAvgs


class ResultCalculator:

    def Calculate_yearly_results(self, temp_readings):
        final_result = YearlyTempResultData(temp_readings[0].date, temp_readings[0].high_temp, temp_readings[0].date,
                                            temp_readings[0].low_temp, temp_readings[0].date, temp_readings[0].humidity)
        for reading in temp_readings:
            if reading.high_temp and int(reading.high_temp) > int(final_result.highest_temp):
                final_result.date_highest_temp = reading.date
                final_result.highest_temp = reading.high_temp
            if reading.low_temp and int(reading.low_temp) < int(final_result.lowest_temp):
                final_result.date_lowest_temp = reading.date
                final_result.lowest_temp = reading.low_temp
            if reading.humidity and int(reading.humidity) > int(final_result.top_humidity):
                final_result.date_humidity = reading.date
                final_result.top_humidity = reading.humidity
        return final_result

    def calculate_avg(self, readings):
        high_sum = 0
        low_sum = 0
        humidity_sum = 0
        for reading in readings:
            if reading.high_temp:
                high_sum += int(reading.high_temp)
            if reading.low_temp:
                low_sum += int(reading.low_temp)
            if reading.mean_humidity:
                humidity_sum += int(reading.mean_humidity)
        high_avg = high_sum / len(readings)
        low_avg = low_sum / len(readings)
        avg_humid = humidity_sum / len(readings)
        avg_monthly_result = MonthlyAvgs(high_avg, low_avg, avg_humid)
        return avg_monthly_result
