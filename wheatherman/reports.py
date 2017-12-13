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

        maximum_temperature = max(maximum_termperatures, key=lambda x: x.maximum_temperature)
        minimum_temperature = min(minimum_termperatures, key=lambda x: x.minimum_temperature)
        maximum_humidity = max(humidity_termperatures, key=lambda x: x.maximum_humidity)
        self.maximum_temperature = maximum_temperature.maximum_temperature
        self.maximum_temperature_date = maximum_temperature.tempetaure_date
        self.minimum_temperature = minimum_temperature.minimum_temperature
        self.minimum_temperature_date = minimum_temperature.tempetaure_date
        self.maximum_humidity = maximum_humidity.maximum_humidity
        self.maximum_humidity_date = maximum_humidity.tempetaure_date

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
        maximum_termperatures = [weather for weather in wheather_data if
                                 weather.maximum_temperature is not None and weather.minimum_temperature is not None]
        for node in maximum_termperatures:
            bar = Barchart(chart_date=node.tempetaure_date, max_temp=node.maximum_temperature,
                           min_temp=node.minimum_temperature)
            self.barchart.append(bar)
