from statistics import mean


class DataCalculator:

    def monthly_analysis(self, extracted_data, date):
        records = [record for record in extracted_data if
                   record.date.year == date.year and
                   record.date.month == date.month]
        high_temp = mean(records.max_temp for records in records)
        min_temp = mean(records.min_temp for records in records)
        mean_humidity = mean(records.avg_humidity for records in records)

        return [high_temp, min_temp, mean_humidity]

    def yearly_analysis(self, extracted_data, date):
        records = [record for record in extracted_data if record.date.year == date.year]
        max_temp = max(records, key=lambda record: record.max_temp)
        min_temp = max(records, key=lambda record: record.min_temp)
        max_humidity = max(records, key=lambda record: record.max_humidity)

        return [max_temp, min_temp, max_humidity]

    def monthly_records(self, extracted_data, date):
        return [record for record in extracted_data if
                record.date.year == date.year and
                record.date.month == date.month]
