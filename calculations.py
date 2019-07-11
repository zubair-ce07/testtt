from statistics import mean

class Calculations:


    def rec_monthly(self,weather_data,date):
        return [
            record for record in weather_data if
            record.date.year == date.year and
            record.date.month == date.month
            ]

    def report_monthly(self, weather_data, date):
        records = self.rec_monthly(weather_data, date)
        high_temp = mean(records.highest_temp for records in records)
        min_temp = mean(records.lowest_temp for records in records)
        mean_humidity = mean(records.avg_humidity for records in records)

        return [high_temp, min_temp, mean_humidity]

    def report_yearly(self, weather_data, year):
        records = [record for record in weather_data if record.date.year == year]
        max_temp_record = max(records, key=lambda record: record.highest_temp)
        min_temp_record = max(records, key=lambda record: record.lowest_temp)
        max_humidity_record = max(records, key=lambda record: record.highest_humidity)

        return [max_temp_record, min_temp_record, max_humidity_record]
