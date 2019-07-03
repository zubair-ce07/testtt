import statistics


from reportgenerator import HighLowResult, AvgTemperatureResult
from reportgenerator import ReportPrinter


class ReportGenerator:

    def __init__(self, weather_records):
        self.weather_parser = weather_records
        self.weather_printer = ReportPrinter()

    def high_low_temperature(self, year):

        weather_data = self.weather_parser.weather_records_of(year=year)
        max_temp_record = max(weather_data, key=lambda x: x.max_temp)
        max_humidity_record = max(weather_data, key=lambda x: x.max_humidity)
        min_temp_record = min(weather_data, key=lambda x: x.min_temp)

        output = HighLowResult(max_temp_record, max_humidity_record, min_temp_record)
        self.weather_printer.high_low_temperature_printer(output)

    def avg_temperature(self, year, month):

        weather_data = self.weather_parser.weather_records_of(year=year, month=month)

        max_temps = [d.max_temp for d in weather_data if d.max_temp]
        min_temps = [d.min_temp for d in weather_data if d.min_temp]
        mean_humidities = [d.mean_humidity for d in weather_data if d.mean_humidity]

        avg_max_temp = int(statistics.mean(max_temps))
        avg_min_temp = int(statistics.mean(min_temps))
        avg_mean_humidity = int(statistics.mean(mean_humidities))

        output = AvgTemperatureResult(avg_max_temp, avg_mean_humidity, avg_min_temp)
        self.weather_printer.avg_temperature_printer(output)

    def high_low_temperature_single_graph(self, year, month):

        weather_data = self.weather_parser.weather_records_of(year=year, month=month)
        self.weather_printer.single_graph_printer(weather_data)

    def high_low_temperature_dual_graph(self, year, month):

        weather_data = self.weather_parser.weather_records_of(year=year, month=month)
        self.weather_printer.dual_graph_printer(weather_data)
