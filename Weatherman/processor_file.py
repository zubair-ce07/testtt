from weather_analyzer import WeatherAnalyzer
from weather_readings_reader import WeatherReadingsReader
from report_generator import ReportGenerator


class Driver:

    def __init__(self, args):
        Driver.run(args)

    @staticmethod
    def run(args):
        my_path = args.directory
        if args.type_e:
            weather_readings = WeatherReadingsReader.read_readings(my_path, args.type_e)
            Driver.process_annual_report(args.type_e, weather_readings)
        if args.type_a:
            year, month = args.type_a.split('/')
            month_name = Driver.month_translation[int(month)]
            weather_readings = WeatherReadingsReader.read_readings(
                my_path, int(year), month_name)
            Driver.process_month_report(int(month), int(year), weather_readings)
        if args.type_c:
            year, month = args.type_c.split('/')
            month_name = Driver.month_translation[int(month)]
            weather_readings = WeatherReadingsReader.read_readings(
                my_path, int(year), month_name)
            Driver.process_dual_bar_report(args.type_c, weather_readings)
        if args.type_d:
            year, month = args.type_d.split('/')
            month_name = Driver.month_translation[int(month)]
            weather_readings = WeatherReadingsReader.read_readings(
                my_path, int(year), month_name)
            Driver.process_single_bar_report(args.type_d, weather_readings)

    @staticmethod
    def process_annual_report(year, weather_readings):
        highest_hum = highest_temp = lowest_temp = None
        if weather_readings:
            highest_temp = WeatherAnalyzer.highest_temp_of_year(weather_readings)
            lowest_temp = WeatherAnalyzer.lowest_temp_of_year(weather_readings)
            highest_hum = WeatherAnalyzer.highest_hum_of_year(weather_readings)
        ReportGenerator.annual_report(year, highest_hum, highest_temp, lowest_temp)

    @staticmethod
    def process_month_report(month, year, weather_readings):
        max_avg_temp = min_avg_temp = mean_avg_hum = None
        if weather_readings:
            max_avg_temp = WeatherAnalyzer.highest_avg_temp_of_month(weather_readings)
            min_avg_temp = WeatherAnalyzer.lowest_avg_temp_of_month(weather_readings)
            mean_avg_hum = WeatherAnalyzer.average_mean_humidity_of_month(weather_readings)
        ReportGenerator.month_report(month, year, max_avg_temp, min_avg_temp, mean_avg_hum)

    @staticmethod
    def process_dual_bar_report(argument, weather_readings):
        year, month = argument.split('/')
        ReportGenerator.dual_bar_chart_report(int(year), int(month), weather_readings)

    @staticmethod
    def process_single_bar_report(argument, weather_readings):
        year, month = argument.split('/')
        ReportGenerator.single_bar_chart_report(int(year), int(month), weather_readings)

    month_translation = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                         7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
