
class ResultCalculations:
    """
    Class for the calculation of the results to be displays
    on the basis of the data read from the file according to
    the command line arguments.
    """

    def __init__(self):
        pass

    def set_data(self, data):
        """Setter function for data"""
        self.data = data

    def calculate_highest_temp(self):
        """Calculate highest temperature for the yearly data"""
        max_temp = 0
        for item in self.data:
            if self.data[item]['Max TemperatureC'] != "" and float(
                    self.data[item]['Max TemperatureC']) > max_temp:
                max_temp = float(self.data[item]['Max TemperatureC'])
                info = item

        data = [max_temp, info]
        return data

    def calculate_lowest_temp(self):
        """Calculate minimum temperature for the yearly data"""
        min_temp = 0
        for i, item in enumerate(self.data):
            if i == 0:
                min_temp = float(self.data[item]['Min TemperatureC'])
            if self.data[item]['Min TemperatureC'] != "" and float(
                    self.data[item]['Min TemperatureC']) < min_temp:
                min_temp = float(self.data[item]['Min TemperatureC'])
                info = item

        data = [min_temp, info]
        return data

    def calculate_highest_humidity(self):
        """Calculate minimum humidity for the yearly data"""
        max_humid = 0
        for item in self.data:
            if self.data[item]['Max Humidity'] != "" and float(
                    self.data[item]['Max Humidity']) > max_humid:
                max_humid = float(self.data[item]['Max Humidity'])
                info = item
        data = [max_humid, info]
        return data

    def calculate_average(self):
        """ 
        Calculate average maximum temperature, average minimum temperature
        and average mean humidity.
        """
        avg_max_temp, avg_min_temp, avg_mean_humidity = 0, 0, 0

        for i, item in enumerate(self.data):

            if self.data[item]['Max Humidity'] != "":
                avg_max_temp = avg_max_temp + float(
                    self.data[item]['Max TemperatureC'])

                avg_min_temp = avg_min_temp + float(
                    self.data[item]['Min TemperatureC'])

                avg_mean_humidity = avg_mean_humidity + float(
                    self.data[item]['Mean Humidity'])

        avg_max_temp = avg_max_temp / (i + 1)
        avg_min_temp = avg_min_temp / (i + 1)
        avg_mean_humidity = avg_mean_humidity / (i + 1)

        data = [avg_max_temp, avg_min_temp, avg_mean_humidity]

        return data

    def get_max_and_min_temperature(self):

        return_data = {}

        for item in self.data:

            req_data = {
                "Max Temperature": self.data[item]['Max TemperatureC'],
                "Min Temperature": self.data[item]['Min TemperatureC']
            }
            return_data[item] = req_data

        return return_data
