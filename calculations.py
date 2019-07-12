from statistics import mean
from datetime import datetime

class Calculations:

    def calculations_yearly(self, total_records, year):

        records = [record for record in total_records if record.date.year == year]
        highest = max(records, key=lambda record: record.highest_temp)
        lowest = min(records, key=lambda record: record.lowest_temp)
        humidity = max(records, key=lambda record: record.highest_humidity)

        return [highest, lowest, humidity]

    def record_month(self, total_records, date):
        return [record for record in total_records if
                record.date.year == date.year and
                record.date.month == date.month]

    def calculations_montly(self, total_records, date):

        records = self.record_month(total_records, date)
        highest = mean(records.highest_temp for records in records)
        lowest = mean(records.lowest_temp for records in records)
        mean_humidity = mean(records.avg_humidity for records in records)

        return [highest, lowest, mean_humidity]



