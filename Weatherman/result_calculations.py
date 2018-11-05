class ResultCalculations:
    """ Class for the calculation of the results to be displayed
    on the basis of the details """

    def find_yearly_data(self, records, year):
        matched_records = [record for record in records if record.date.year == year]
        if matched_records:
            instance_max_temp = max(matched_records, key=lambda instance: instance.max_temperature)
            instance_min_temp = min(matched_records, key=lambda instance: instance.min_temperature)
            instance_max_humidity = max(matched_records, key=lambda instance: instance.max_humidity)

            return [instance_max_temp, instance_min_temp, instance_max_humidity]

    def find_monthly_data(self, records, date):
        return [
            record for record in records if date.year == record.date.year and date.month == record.date.month]

    def calculate_average(self, records, date):
        matched_records = self.find_monthly_data(records, date)
        if matched_records:
            avg_max_temp = sum([
                instance.max_temperature for instance in matched_records]) / len(matched_records)
            avg_min_temp = sum([
                instance.min_temperature for instance in matched_records]) / len(matched_records)
            avg_mean_humidity = sum([
                instance.mean_humidity for instance in matched_records]) / len(matched_records)

            return [avg_max_temp, avg_min_temp, avg_mean_humidity]
