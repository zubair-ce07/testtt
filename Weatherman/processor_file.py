import weather_analyzer
import weather_readings_reader
import analysis_results
import report_generator


def process_annual_report(year, data):
    highest_temp = weather_analyzer.WeatherAnalyzer.highest_temp_of_year(data)
    lowest_temp = weather_analyzer.WeatherAnalyzer.lowest_temp_of_year(data)
    highest_hum = weather_analyzer.WeatherAnalyzer.highest_hum_of_year(data)
    date_max_annual_hum = [highest_hum.day, highest_hum.month, highest_hum.year]
    date_max_annual_temp = [highest_temp.day, highest_temp.month, highest_temp.year]
    date_min_annual_temp = [lowest_temp.day, lowest_temp.month, lowest_temp.year]
    max_annual_hum = highest_hum.highest_hum
    min_annual_temp = lowest_temp.lowest_temp
    max_annual_temp = highest_temp.highest_temp
    results = {'date_max_annual_temp': date_max_annual_temp, 'date_max_annual_hum': date_max_annual_hum,
               'date_min_annual_temp': date_min_annual_temp, 'max_annual_hum': max_annual_hum,
               'max_annual_temp': max_annual_temp, 'min_annual_temp': min_annual_temp}
    results = analysis_results.AnalysisResults(results)
    report_generator.ReportGenerator.annual_report(year, results)


def process_month_report(month, year, data):
    max_avg_temp = weather_analyzer.WeatherAnalyzer.highest_avg_temp_of_month(data)
    min_avg_temp = weather_analyzer.WeatherAnalyzer.lowest_avg_temp_of_month(data)
    mean_avg_hum = weather_analyzer.WeatherAnalyzer.average_mean_humidity_of_month(data)
    results = {'mean_avg_hum': mean_avg_hum,
               'min_avg_temp': min_avg_temp,
               'max_avg_temp': max_avg_temp}
    results = analysis_results.AnalysisResults(results)
    report_generator.ReportGenerator.month_report(month, year, results)


def process_dual_bar_report(argument, data):
    year, month = argument.split('/')
    report_generator.ReportGenerator.dual_bar_chart_report(int(year), int(month), data)


def process_single_bar_report(argument, data):
    year, month = argument.split('/')
    report_generator.ReportGenerator.single_bar_chart_report(int(year), int(month), data)


def is_valid(argument):
    try:
        year, month = argument.split('/')
        if int(year) in range(1900, 2019) and int(month) in range(1, 13):
            return argument
        else:
            report_generator.ReportGenerator.display_error_msg()
            return False
    except:
        report_generator.ReportGenerator.display_error_msg()
        return False


def month_resolution(month_number):
    month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                  7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    return month_dict[month_number]


def run(args):
    my_path = args.directory
    if args.type_e:
        weather_readings = weather_readings_reader.WeatherReadingsReader.read_readings(my_path, args.type_e)
        if len(weather_readings) > 0:
            process_annual_report(args.type_e, weather_readings)
        else:
            report_generator.ReportGenerator.display_empty_error_msg()
    if args.type_a:
        year, month = args.type_a.split('/')
        month_name = month_resolution(int(month))
        weather_readings = weather_readings_reader.WeatherReadingsReader.read_readings(
            my_path, int(year), month_name)
        if len(weather_readings) > 0:
            process_month_report(int(month), int(year), weather_readings)
        else:
            report_generator.ReportGenerator.display_empty_error_msg()
    if args.type_c:
        year, month = args.type_c.split('/')
        month_name = month_resolution(int(month))
        weather_readings = weather_readings_reader.WeatherReadingsReader.read_readings(
            my_path, int(year), month_name)
        if len(weather_readings) > 0:
            process_dual_bar_report(args.type_c, weather_readings)
        else:
            report_generator.ReportGenerator.display_empty_error_msg()
    if args.type_d:
        year, month = args.type_d.split('/')
        month_name = month_resolution(int(month))
        weather_readings = weather_readings_reader.WeatherReadingsReader.read_readings(
            my_path, int(year), month_name)
        if len(weather_readings) > 0:
            process_single_bar_report(args.type_d, weather_readings)
        else:
            report_generator.ReportGenerator.display_empty_error_msg()