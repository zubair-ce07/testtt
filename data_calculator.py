from statistics import mean


class DataCalculator:

    def monthly_records(self, weather_records, date):
        return [record for record in weather_records if
                record.date.year == date.year and
                record.date.month == date.month]

    def monthly_analysis(self, weather_records, date):
        records = self.monthly_records(weather_records, date)
        high_temp = mean(records.max_temp for records in records)
        min_temp = mean(records.min_temp for records in records)
        mean_humidity = mean(records.avg_humidity for records in records)

        return [high_temp, min_temp, mean_humidity]

    def yearly_analysis(self, weather_records, year):
        records = [record for record in weather_records if record.date.year == year]
        max_temp_record = max(records, key=lambda record: record.max_temp)
        min_temp_record = max(records, key=lambda record: record.min_temp)
        max_humidity_record = max(records, key=lambda record: record.max_humidity)

        return [max_temp_record, min_temp_record, max_humidity_record]
