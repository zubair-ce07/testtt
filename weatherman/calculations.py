

class CalculateResults:
        """Calculates the required results"""

        def yearly_result(self, list_of_records):

            max_temp = max(list_of_records, key=lambda rec: rec.max_temperature)
            min_temp = min(list_of_records, key=lambda rec: rec.min_temperature)
            max_humidity = max(list_of_records, key=lambda rec: rec.max_humidity)
            return max_temp, min_temp, max_humidity

        def average_result(self, list_of_records):

            max_temperature = [record.max_temperature for record in list_of_records if record.max_temperature]
            min_temperature = [record.min_temperature for record in list_of_records if record.min_temperature]
            mean_temperature = [record.mean_temperature for record in list_of_records if record.mean_temperature]

            length_of_records = len(list_of_records)
            avg_max_temp = sum(max_temperature) // length_of_records
            avg_min_temp = sum(min_temperature) // length_of_records
            avg_mean_humidity = sum(mean_temperature) // length_of_records

            return avg_max_temp, avg_min_temp, avg_mean_humidity

        def monthly_graph(self, list_of_records):

            max_temp_highest = max(list_of_records, key=lambda record: record.max_temperature)
            min_temp_lowest = min(list_of_records, key=lambda record: record.min_temperature)
            return max_temp_highest, min_temp_lowest
