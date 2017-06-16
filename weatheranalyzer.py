from weatherfilereader import WeatherFilesReader
from resultsprinter import WeatherReportPrinter


class WeatherReporter(object):

    weather_file_reader = None
    report_printer = None

    def __init__(self):
        self.weather_file_reader = WeatherFilesReader()
        self.report_printer = WeatherReportPrinter()

    def start(self, user_inputs):
        self.weather_file_reader.set_directory(user_inputs.dir)
        if user_inputs.e:
            report = self.records_by_year(user_inputs.e)
            self.report_printer.highest_temp(report['max_temp'])
            self.report_printer.lowest_temp(report['min_temp'])
            self.report_printer.highest_humid(report['max_humid'])
        if user_inputs.a:
            year, month = user_inputs.a.split('/')
            report = self.records_by_month(year, month)
            self.report_printer.mean_highest_temp(report['avg_max_temp'])
            self.report_printer.mean_lowest_temp(report['avg_min_temp'])
            self.report_printer.mean_highest_humid(report['avg_max_humid'])
        if user_inputs.c:
            year, month = user_inputs.c.split('/')
            records = self.weather_file_reader.read_by_month(year, month)
            self.report_printer.display_chart(records)
        if user_inputs.b:
            year, month = user_inputs.b.split('/')
            records = self.weather_file_reader.read_by_month(year, month)
            self.report_printer.display_singleline_chart(records)

    def get_max_temp(self, results):
        max_temp = max(results, key=lambda row: int(results[row]['max_temp']))
        return {max_temp:results[max_temp]}

    def get_min_temp(self, results):
        min_temp = min(results, key=lambda record: int(results[record]['min_temp']))
        return {min_temp:results[min_temp]}

    def get_max_humid(self, results):
        max_humid = max(results, key=lambda record: int(results[record]['max_humid']))
        return {max_humid:results[max_humid]}

    def get_avg_by(self, results, key):
        sum = 0
        for row in results.values():
            sum += int(row[key])
        return sum / len(results)

    def records_by_year(self, year):
        results = self.weather_file_reader.read_by_year(year)
        return {'max_temp':self.get_max_temp(results),
                'min_temp':self.get_min_temp(results),
                'max_humid':self.get_max_humid(results)
                }

    def records_by_month(self, year, month):
        results = self.weather_file_reader.read_by_month(year, month)
        return {'avg_max_temp':self.get_avg_by(results, 'max_temp'),
                'avg_min_temp':self.get_avg_by(results, 'min_temp'),
                'avg_max_humid':self.get_avg_by(results, 'max_humid'),
                }

    def mean(self, temperatures):
        return sum(temperatures) / len(temperatures)