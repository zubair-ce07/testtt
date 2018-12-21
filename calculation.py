class Calculations:
    def calculate_year_values(self, year_weather_data):
        result = {
            "max_temp_day": self.find_max_temp_day(year_weather_data),
            "min_temp_day": self.find_min_temp_day(year_weather_data),
            "max_humidity_day": self.find_max_humid_day(year_weather_data)
        }
        return result

    def calculate_month_values(self, month_data):
        result = {
            "max_day": self.find_max_temp_day(month_data),
            "min_day": self.find_min_temp_day(month_data)
        }
        return result

    def calculate_average_values(self, month_data):
        highest_temp_record = [float(day.max_temp) if day.max_temp else 0 for day in month_data]
        lowest_temp_record = [float(day.min_temp) if day.min_temp else 0 for day in month_data]
        highest_humidity_record = [float(day.max_humidity) if day.max_humidity else 0 for day in month_data]

        result = {
            "highest_temp": self.find_average(highest_temp_record),
            "lowest_temp": self.find_average(lowest_temp_record),
            "highest_humidity": self.find_average(highest_humidity_record)
        }
        return result

    def find_max_temp_day(self, record):
        max_value_index = max([int(v.max_temp) for v in record if int(v.max_temp) > 0])
        return record[max_value_index]

    def find_min_temp_day(self, record):
        min_index = min([int(v.min_temp) for v in record if int(v.min_temp) > 0])
        return record[min_index]

    def find_max_humid_day(self, record):
        max_humid_index = max([int(v.max_humidity) for v in record if int(v.max_humidity) > 0])
        return record[max_humid_index]

    def find_average(self, record):
        return sum(record) // len(record)
