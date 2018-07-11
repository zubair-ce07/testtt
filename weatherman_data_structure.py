class readings_holder:

    def __init__(self, features):
        if 'PKT' in features.keys():
            self.pkt = features['PKT']
        else:
            self.pkt = features['PKST']
        self.max_temp = int(features['Max TemperatureC'])
        self.min_temp = int(features['Min TemperatureC'])
        self.mean_temp = int(features['Mean TemperatureC'])
        self.max_humidity = int(features['Max Humidity'])
        self.min_humidity = int(features[' Min Humidity'])
        self.mean_humidity = int(features[' Mean Humidity'])


class calculation_holder:

    def __init__(self, readings):
        self.maximum_temperature = readings[0]
        self.minimum_temperature = readings[1]
        self.maximum_humidity = readings[2]
        self.maximum_temperature_day = readings[3]
        self.minimum_temperature_day = readings[4]
        self.maximum_humidity_day = readings[5]
        self.max_mean_temperature = readings[6]
        self.min_mean_temperature = readings[7]
        self.average_mean_humidity = readings[8]


class colors:

    RED = "\u001b[31m"
    MAGENTA = "\u001b[35m"
    BLUE = "\u001b[34m"
    RESET = "\u001b[0m"
    GREEN = "\u001b[32m"
