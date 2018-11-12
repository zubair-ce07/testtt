class WeatherDataAnalysis:

    def find_max(self, records, attribute):
        return max(records, key=lambda record: record[attribute])

    def find_min(self, records, attribute):
        return min(records, key=lambda record: record[attribute])

    def find_average(self, records, attribute):
        records = [record[attribute] for record in records]
        return sum(records)//len(records)

    def calculate_yearly_report(self, year_records):
        return {
            'lowest': self.find_min(year_records, 'min_temp'),
            'highest': self.find_max(year_records, 'max_temp'),
            'humidity': self.find_max(year_records, 'max_humidity'),
        }

    def calculate_monthly_report(self, month_records):
        return {
            'average_max_temp': self.find_average(month_records, 'max_temp'),
            'average_min_temp': self.find_average(month_records, 'min_temp'),
            'average_mean_humidity': self.find_average(month_records, 'mean_humidity')
        }
