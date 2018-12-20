class ResultCalculations:
    """ Class for the calculation of the results to be displayed
    on the basis of the details """

    def find_yearly_data(self, records, year):
        records = [record for record in records if record.date.year == year]

        if not records:
            return

        max_temp_record = max(records, key=lambda record: record.max_temperature)
        min_temp_record = min(records, key=lambda record: record.min_temperature)
        max_humidity_record = max(records, key=lambda record: record.max_humidity)

        return max_temp_record, min_temp_record, max_humidity_record

    def find_monthly_data(self, records, date):
        return [
            record for record in records if date.year == record.date.year and date.month == record.date.month]

    def calculate_average(self, records, date):
        records = self.find_monthly_data(records, date)

        if not records:
            return

        avg_max_temp = sum([record.max_temperature for record in records]) // len(records)
        avg_min_temp = sum([record.min_temperature for record in records]) // len(records)
        avg_mean_humidity = sum([record.mean_humidity for record in records]) // len(records)

        return avg_max_temp, avg_min_temp, avg_mean_humidity
