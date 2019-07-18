from statistics import mean


class DataCalculator:

    def monthly_records(self, weather_records, date):
        return [row for row in weather_records if row.date.year == date.year and row.date.month == date.month]

    def get_max_min(self, weather_records, date):
        records = self.monthly_records(weather_records, date)
        highest_temp = mean(records.highest_temp for records in records)
        lowest_temp = mean(records.lowest_temp for records in records)
        avg_humidity = mean(records.avg_humidity for records in records)

        return [highest_temp, lowest_temp, avg_humidity]

    def month_average(self, weather_records, year):
        records = [record for record in weather_records if record.date.year == year]
        max_temp_record = max(records, key=lambda record: record.highest_temp)
        min_temp_record = max(records, key=lambda record: record.lowest_temp)
        max_humidity_record = max(records, key=lambda record: record.highest_humidity)

        return [max_temp_record, min_temp_record, max_humidity_record]
