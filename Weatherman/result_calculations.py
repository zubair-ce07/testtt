class ResultCalculations:
    """ Class for the calculation of the results to be displayed
    on the basis of the details """

    def find_yearly_data(self, records, year):
        records = [record for record in records if record.date.year == year]

        if not records:
            return

        instance_max_temp = max(records, key=lambda record: record.max_temperature)
        instance_min_temp = min(records, key=lambda record: record.min_temperature)
        instance_max_humidity = max(records, key=lambda record: record.max_humidity)

        return instance_max_temp, instance_min_temp, instance_max_humidity

    def find_monthly_data(self, records, date):
        return [
            record for record in records if date.year == record.date.year and date.month == record.date.month]

    def calculate_average(self, records, date):
        records = self.find_monthly_data(records, date)

        if not records:
            return

        avg_max_temp = sum([
            record.max_temperature for record in records]) // len(records)
        avg_min_temp = sum([
            record.min_temperature for record in records]) // len(records)
        avg_mean_humidity = sum([
            record.mean_humidity for record in records]) // len(records)

        return avg_max_temp, avg_min_temp, avg_mean_humidity
