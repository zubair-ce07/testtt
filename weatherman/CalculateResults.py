from yearly_temp import TemperatureResults


class Results:

    def Calculate_yearly_results(self, temp_readings):
        final_result = TemperatureResults(temp_readings[0].date, temp_readings[0].high_temp, temp_readings[0].date,
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
        high_avg = int(sum(map(self.give_high_temp, [reading for reading in readings])) / len(readings))
        low_avg = int(sum(map(self.give_low_temp, [reading for reading in readings])) / len(readings))
        avg_humid = int(sum(map(self.give_humidity, [reading for reading in readings])) / len(readings))
        avg_monthly_result = TemperatureResults("", high_avg, "", low_avg, "", avg_humid)
        return avg_monthly_result

    def give_high_temp(self, reading):
        if reading.high_temp:
            return int(reading.high_temp)
        else:
            return 0

    def give_low_temp(self, reading):
        if reading.low_temp:
            return int(reading.low_temp)
        else:
            return 0

    def give_humidity(self, reading):
        if reading.mean_humidity:
            return int(reading.mean_humidity)
        else:
            return 0
