from statistics import mean


class Calculations:

    def calculations_yearly(self, weather_records, year):
        records = [record for record in weather_records if record.date.year == year]
        max_temp_record = max(records, key=lambda record: record.highest_temp)
        min_temp_record = max(records, key=lambda record: record.lowest_temp)
        max_humidity_record = max(records, key=lambda record: record.highest_humidity)

        return [max_temp_record, min_temp_record, max_humidity_record]

    def record_month(self, weather_records, date):
        return [record for record in weather_records if
                record.date.year == date.year and
                record.date.month == date.month]

    def calculations_montly(self, weather_records, date):
        records = self.record_month(weather_records, date)
        highest_temp = mean(records.highest_temp for records in records)
        lowest_temp = mean(records.lowest_temp for records in records)
        mean_humidity = mean(records.avg_humidity for records in records)

        return [highest_temp, lowest_temp, mean_humidity]
