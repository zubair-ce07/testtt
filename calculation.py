import collections


class Calculation:
    def __init__(self):
        self.yearly_cal = collections.defaultdict(lambda: 0)
        self.monthly_cal = collections.defaultdict(lambda: 0)
        self.monthly_barchart_cal = collections.defaultdict(lambda: 0)

    def yearly_calculation(self, weather_records):
        max_temp = []
        min_temp = []
        humiditi = []
        date = []
        for record in weather_records:
            date.append(record.date)
            max_temp.append(record.max_temperature)
            min_temp.append(record.min_temperature)
            humiditi.append(record.max_humidity)

        max_temperatures = []
        for x in max_temp:
            max_temperatures.append(float(x) if x else -100)
        min_temperatures = []
        for x in min_temp:
            min_temperatures.append(float(x)  if x else 10000)

        humidity = []
        for x in humiditi:
            humidity.append(float(x) if x else -100)


        max_temperature = max(max_temperatures)
        max_index = max_temperatures.index(max_temperature)
        min_temperature = min(min_temperatures)
        min_index = min_temperatures.index(min_temperature)
        max_humidity = max(humidity)
        humid_index = humidity.index(max_humidity)

        self.yearly_cal["max_temp"] = str(max_temperature)
        self.yearly_cal["max_temp_date"] = str(date[max_index])

        self.yearly_cal["min_temp"] = str(min_temperature)
        self.yearly_cal["min_temp_date"] = str(date[min_index])

        self.yearly_cal["max_humidity"] = str(max_humidity)
        self.yearly_cal["max_humidity_date"] = str(date[humid_index])
        return self.yearly_cal

    def monthly_report_calculation(self, weather_records):
        max_temp = []
        min_temp = []
        humiditi = []

        for record in weather_records:
            max_temp.append(record.max_temperature)
            min_temp.append(record.min_temperature)
            humiditi.append(record.mean_humidity)


        max_temperatures = [float(x) for x in max_temp if x]
        min_temperatures = [float(x) for x in min_temp if x]
        humidity = [float(x) for x in humiditi if x]

        avg_max_temp = int(sum(max_temperatures) / len(max_temperatures))
        avg_min_temp = int(sum(min_temperatures) / len(min_temperatures))
        avg_mean_humidity = int(sum(humidity) / float(len(humidity)))

        self.monthly_cal["age_max_temp"] = avg_max_temp
        self.monthly_cal["age_min_temp"] = avg_min_temp
        self.monthly_cal["age_mean_humidity"] = avg_mean_humidity
        return self.monthly_cal

    def monthly_barchart_calculation(self, weather_records):

        max_temp = []
        min_temp = []
        for record in weather_records:
            max_temp.append(record.max_temperature)
            min_temp.append(record.min_temperature)


        max_temperatures = []
        for x in max_temp:
            max_temperatures.append(int(x) if x else 0)
        min_temperatures = []
        for x in min_temp:
            min_temperatures.append(int(x) if x else 0)

        self.monthly_barchart_cal["max_temp"] = max_temperatures
        self.monthly_barchart_cal["min_temp"] = min_temperatures
        return self.monthly_barchart_cal
