class Calculations:
    def year_peak_calculation(self, year_weather_data):
        result = {
            "max_temp_day": self.max_day(year_weather_data),
            "min_temp_day": self.min_day(year_weather_data),
            "max_humidity_day": self.max_humid_day(year_weather_data)
        }
        return result

    def month_peak_calculation(self, month_data):
        result = {
            "max_day": self.max_day(month_data),
            "min_day": self.min_day(month_data)
        }
        return result

    def month_average_calculation(self, month_data):
        highest_temp_record = [float(day.max_temp) if day.max_temp else 0 for day in month_data]
        lowest_temp_record = [float(day.min_temp) if day.min_temp else 0 for day in month_data]
        highest_humidity_record = [float(day.max_humidity) if day.max_humidity else 0 for day in month_data]

        result = {
            "highest_temp": self.average(highest_temp_record),
            "lowest_temp": self.average(lowest_temp_record),
            "highest_humidity": self.average(highest_humidity_record)
        }
        return result

    def max_day(self, record):
        max_index = max([int(v.max_temp) for v in record if int(v.max_temp) > 0])
        return record[max_index]

    def min_day(self, record):
        min_index = min([int(v.min_temp) for v in record if int(v.min_temp) > 0])
        return record[min_index]

    def max_humid_day(self, record):
        max_humid_index = max([int(v.max_humidity) for v in record if int(v.max_humidity) > 0])
        return record[max_humid_index]

    def average(self, record):
        return sum(record) // len(record)
