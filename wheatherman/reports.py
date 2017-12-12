import statistics
from wheatherman.barchart import Barchart


class Reports:
    maximum_temperature = 0
    minimum_temperature = 0
    maximum_humidity = 0
    maximum_temperature_date = ""
    minimum_temperature_date = ""
    maximum_humidity_date = ""
    maximum_temperature_mean = 0
    minimum_temperature_mean = 0
    average_humidity = 0
    barchart = []
    barchart_bonus = []

    def maximum_temperature_report(self, wheather_data):
        maximum_termperatures = [weather for weather in wheather_data if
                                 weather.maximum_temperature is not None]
        minimum_termperatures = [weather for weather in wheather_data if
                                 weather.minimum_temperature is not None]
        humidity_termperatures = [weather for weather in wheather_data if
                                  weather.maximum_humidity is not None]

        maximum_temperature_object = max(maximum_termperatures, key=lambda x: x.maximum_temperature)
        minimum_temperature_object = max(minimum_termperatures, key=lambda x: x.minimum_temperature)
        maximum_humidity_object = max(humidity_termperatures, key=lambda x: x.maximum_humidity)
        self.maximum_temperature = maximum_temperature_object.maximum_temperature
        self.maximum_temperature_date = maximum_temperature_object.tempetaure_date
        self.minimum_temperature = minimum_temperature_object.minimum_temperature
        self.minimum_temperature_date = minimum_temperature_object.tempetaure_date
        self.maximum_humidity = maximum_humidity_object.maximum_humidity
        self.maximum_humidity_date = maximum_humidity_object.tempetaure_date

    def average_temperature_report(self, wheather_data):
        maximum_termperatures = [node.maximum_temperature
                                 for node in wheather_data
                                 if node.maximum_temperature is not None]
        minimum_termperatures = [node.minimum_temperature
                                 for node in wheather_data
                                 if node.minimum_temperature is not None]
        average_humidities = [node.average_humidity
                              for node in wheather_data
                              if node.average_humidity is not None]
        self.maximum_temperature_mean = statistics.mean(maximum_termperatures)
        self.minimum_temperature_mean = statistics.mean(minimum_termperatures)
        self.average_humidity = statistics.mean(average_humidities)

    def barchart_report(self, wheather_data):
        barchart_max = ""
        barchart_min = ""

        maximum_termperatures = [weather for weather in wheather_data if
                                 weather.maximum_temperature is not None and weather.minimum_temperature is not None]

        for node in maximum_termperatures:
            if node.maximum_temperature:
                barchart_max = "+" * node.maximum_temperature
            if node.minimum_temperature:
                barchart_min = "+" * node.minimum_temperature
            bar = Barchart(barchart_min, barchart_max,
                           node.maximum_temperature,
                           node.minimum_temperature, node.tempetaure_date)
            self.barchart.append(bar)

    def barchart_bonus_report(self, wheather_data):
        red = '\033[31m'
        blue = '\033[34m'
        bar_maximum = ""
        bar_minimum = ""
        for node in wheather_data:
            if node.maximum_temperature:
                bar_maximum = '+' * node.maximum_temperature
                bar_maximum = red + bar_maximum
            if node.minimum_temperature:
                bar_minimum = '+' * node.minimum_temperature
                bar_minimum = blue + bar_minimum
            self.barchart_bonus.append(bar_maximum + bar_minimum)
