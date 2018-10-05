class ResultCalculations:
    """
    Class for the calculation of the results to be displays
    on the basis of the details read from the file according to
    the command line arguments.
    """
    def __init__(self, details={}):
        self.details = details

    def calculate_highest_temp(self):
        """Calculate highest temperature for the yearly details"""
        temp, keys = [], []
        for item in self.details:
            if self.details[item]['Max TemperatureC'] != "":
                temp.append(float(self.details[item]['Max TemperatureC']))
                keys.append(item)
        max_temp = max(temp)
        calculated_details = [max_temp, keys[temp.index(max_temp)]]
        return calculated_details

    def calculate_lowest_temp(self):
        """Calculate minimum temperature for the yearly details"""
        temp, keys = [], []
        for item in self.details:
            if self.details[item]['Min TemperatureC'] != "":
                temp.append(float(self.details[item]['Min TemperatureC']))
                keys.append(item)
        min_temp = min(temp)
        calculated_details = [min_temp, keys[temp.index(min_temp)]]
        return calculated_details

    def calculate_highest_humidity(self):
        """Calculate minimum humidity for the yearly details"""
        humidity, keys = [], []
        for item in self.details:
            if self.details[item]['Max Humidity'] != "":
                humidity.append(float(self.details[item]['Max Humidity']))
                keys.append(item)
        max_humidity = max(humidity)
        calculated_details = [max_humidity, keys[humidity.index(max_humidity)]]
        return calculated_details

    def calculate_average(self):
        """
        Calculate average maximum temperature, average minimum temperature
        and average mean humidity.
        """
        avg_max_temp, avg_min_temp, avg_mean_humidity = [], [], []

        for i, item in enumerate(self.details):
            if self.details[item]['Max Humidity'] != "":
                avg_max_temp.append(float(
                    self.details[item]['Max TemperatureC']))
                avg_min_temp.append(float(
                    self.details[item]['Min TemperatureC']))
                avg_mean_humidity.append(float(
                    self.details[item]['Mean Humidity']))

        avg_max_temp = sum(avg_max_temp) / (i + 1)
        avg_min_temp = sum(avg_min_temp) / (i + 1)
        avg_mean_humidity = sum(avg_mean_humidity) / (i + 1)
        calculated_details = [avg_max_temp, avg_min_temp, avg_mean_humidity]
        return calculated_details

    def get_max_and_min_temperature(self):
        calculated_details = {}
        for item in self.details:
            req_details = {
                "Max Temperature": self.details[item]['Max TemperatureC'],
                "Min Temperature": self.details[item]['Min TemperatureC']
            }
            calculated_details[item] = req_details
        return calculated_details
