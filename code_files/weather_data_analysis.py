class WeatherDataAnalysis:
    def calculate_yearly_report(self, records):
        return {
            'lowest': min(records, key=lambda record: record['min_temp']),
            'highest': max(records, key=lambda record: record['max_temp']),
            'humidity': max(records, key=lambda record: record['max_humidity']),
        }

    def calculate_monthly_report(self, records):
        return {
            'average_max_temp': sum([record['max_temp'] for record in records]) // len(records),
            'average_min_temp': sum([record['min_temp'] for record in records]) // len(records),
            'average_mean_humidity': sum([record['mean_humidity'] for record in records]) // len(records)
        }
