class WeatherRecords:
    """ Class for holding the only required data for each instance """

    def __init__(self, record):
        self.max_temperature = int(record["Max Temperature"])
        self.min_temperature = int(record["Min Temperature"])
        self.max_humidity = int(record["Max Humidity"])
        self.min_humidity = int(record["Min Humidity"])
        self.mean_humidity = int(record["Mean Humidity"])
        self.date = record["Date"]
