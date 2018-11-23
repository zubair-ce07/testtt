

class CalculateResults:
        """Calculates the required results"""

        def hot_cold_humid_day(self, list_of_records):

            """
            reads list_of_records and stores in records list
            and caluclates higest, lowsest and most humid day
            we use key=lambda to compare items by its integer
            values only
            """

            records = []

            for record in list_of_records:
                    records.append(record)

            max_temp = max(records, key=lambda rec: int(rec.max_temperature))
            min_temp = min(records, key=lambda rec: int(rec.min_temperature))
            max_humidity = max(records, key=lambda rec: int(rec.max_humidity))
            return max_temp, min_temp, max_humidity

        def average_max_min_humid_day(self, list_of_records):

            """this function calculates the averages temperatures
               for min max and mean. we are filtering data beacause
               and appending clean data to lists and converting
               list to integer"""
            records = []
            max_temperature = []
            min_temperature = []
            mean_temperature = []
            for record in list_of_records:
                records.append(record)
                max_temperature.append(record.max_temperature)
                min_temperature.append(record.min_temperature)
                mean_temperature.append(record.mean_temperature)

            max_temperature = filter(None, max_temperature)
            max_temperature = list(map(int, max_temperature))

            min_temperature = filter(None, min_temperature)
            min_temperature = list(map(int, min_temperature))

            mean_temperature = filter(None, mean_temperature)
            mean_temperature = list(map(int, mean_temperature))

            avg_max_temp = sum(max_temperature) // len(records)
            avg_min_temp = sum(min_temperature) // len(records)
            avg_mean_humidity = sum(mean_temperature) // len(records)
            return avg_max_temp, avg_min_temp, avg_mean_humidity

        def max_min_temp_day(self, list_of_records):
            """calculates max and min temperature for bar graph"""
            records = []
            for record in list_of_records:
                    records.append(record)

            max_temp_highest = max(records, key=lambda record: record.max_temperature)
            min_temp_lowest = min(records, key=lambda record: record.min_temperature)
            return max_temp_highest, min_temp_lowest
