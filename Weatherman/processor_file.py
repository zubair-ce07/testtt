from weather_analyzer import WeatherAnalyzer
from weather_readings_reader import WeatherReadingsReader
from analysis_results import AnalysisResults
from report_generator import ReportGenerator


class Processor:

    def __init__(self, args):
        Processor.run(args)

    @staticmethod
    def run(args):
        my_path = args.directory
        if args.type_e:
            weather_readings = WeatherReadingsReader.read_readings(my_path, args.type_e)
            Processor.process_annual_report(args.type_e, weather_readings)
        if args.type_a:
            year, month = args.type_a.split('/')
            month_name = Processor.month_resolution(int(month))
            weather_readings = WeatherReadingsReader.read_readings(
                my_path, int(year), month_name)
            Processor.process_month_report(int(month), int(year), weather_readings)
        if args.type_c:
            year, month = args.type_c.split('/')
            month_name = Processor.month_resolution(int(month))
            weather_readings = WeatherReadingsReader.read_readings(
                my_path, int(year), month_name)
            Processor.process_dual_bar_report(args.type_c, weather_readings)
        if args.type_d:
            year, month = args.type_d.split('/')
            month_name = Processor.month_resolution(int(month))
            weather_readings = WeatherReadingsReader.read_readings(
                my_path, int(year), month_name)
            Processor.process_single_bar_report(args.type_d, weather_readings)

    @staticmethod
    def process_annual_report(year, weather_readings):
        results = None
        if weather_readings:
            highest_temp = WeatherAnalyzer.highest_temp_of_year(weather_readings)
            lowest_temp = WeatherAnalyzer.lowest_temp_of_year(weather_readings)
            highest_hum = WeatherAnalyzer.highest_hum_of_year(weather_readings)
            date_max_annual_hum = [highest_hum.day, highest_hum.month, highest_hum.year]
            date_max_annual_temp = [highest_temp.day, highest_temp.month, highest_temp.year]
            date_min_annual_temp = [lowest_temp.day, lowest_temp.month, lowest_temp.year]
            max_annual_hum = highest_hum.highest_hum
            min_annual_temp = lowest_temp.lowest_temp
            max_annual_temp = highest_temp.highest_temp
            results = {'date_max_annual_temp': date_max_annual_temp, 'date_max_annual_hum': date_max_annual_hum,
                       'date_min_annual_temp': date_min_annual_temp, 'max_annual_hum': max_annual_hum,
                       'max_annual_temp': max_annual_temp, 'min_annual_temp': min_annual_temp}
            results = AnalysisResults(results)
        ReportGenerator.annual_report(year, results)

    @staticmethod
    def process_month_report(month, year, weather_readings):
        results = None
        if weather_readings:
            max_avg_temp = WeatherAnalyzer.highest_avg_temp_of_month(weather_readings)
            min_avg_temp = WeatherAnalyzer.lowest_avg_temp_of_month(weather_readings)
            mean_avg_hum = WeatherAnalyzer.average_mean_humidity_of_month(weather_readings)
            results = {'mean_avg_hum': mean_avg_hum,
                       'min_avg_temp': min_avg_temp,
                       'max_avg_temp': max_avg_temp}
            results = AnalysisResults(results)
        ReportGenerator.month_report(month, year, results)

    @staticmethod
    def process_dual_bar_report(argument, weather_readings):
        year, month = argument.split('/')
        ReportGenerator.dual_bar_chart_report(int(year), int(month), weather_readings)

    @staticmethod
    def process_single_bar_report(argument, weather_readings):
        year, month = argument.split('/')
        ReportGenerator.single_bar_chart_report(int(year), int(month), weather_readings)

    @staticmethod
    def is_valid_argument(argument):
        try:
            year, month = argument.split('/')
            if int(year) and int(month) in range(1, 13):
                return argument
            else:
                ReportGenerator.display_argument_error_msg(argument)
                return False
        except:
            ReportGenerator.display_argument_error_msg(argument)
            return False

    @staticmethod
    def month_resolution(month_number):
        month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                      7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        return month_dict[month_number]
