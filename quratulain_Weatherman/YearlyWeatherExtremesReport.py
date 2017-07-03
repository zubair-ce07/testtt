import fnmatch


class YearlyWeatherExtremesReport:
    def __init__(self, records):
        self.records = records

    def generate_report(self):
        self.max_temp_record = max(self.records, key=lambda x: x['maxTemprature'])
        self.min_temp_record = min(self.records, key=lambda x: x['minTemprature'])
        self.max_humid_record = max(self.records, key=lambda x: x['maxHumidity'])

    def print_report(self):
        print("Yearly Weather Report")
        print("Highest: {}C on {} {}".format(
            self.max_temp_record['maxTemprature'],
            self.max_temp_record['month'],
            self.max_temp_record['day']))
        print("Lowest: {}C on {} {}".format(self.min_temp_record['minTemprature'],
            self.min_temp_record['month'],
            self.min_temp_record['day']))
        print("Humidity: {}% on {} {} \n".format(
            self.max_humid_record['maxHumidity'],
            self.max_humid_record['month'],
            self.max_humid_record['day']))
