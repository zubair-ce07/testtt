import sys
from itertools import islice
from populate_weather_readings import WeatherReadingsPopulator as Parser
from calculate_results import ResultsGenerator
from generate_reports import ReportGenerator


def main():
    given_path=sys.argv[1]
    for i in islice(range(len(sys.argv)), 2, None):
        if sys.argv[i] == "-a":
            given_date = sys.argv[i+1].split("/")
            given_year = given_date[0]
            given_month = int(given_date[1])
            weather_file_parser = Parser()
            weather_file_parser.list_files(given_path, sys.argv[i],
                                           given_year, given_month)
            weather_file_parser.populate_weather_readings(given_path)
            results_generator = ResultsGenerator()
            results_generator.generate_results(
                weather_file_parser.weather_readings,
                sys.argv[i])
            report_generator = ReportGenerator(
                sys.argv[i],
                results_generator.generated_results)
            report_generator.print_report()
        elif sys.argv[i] == "-e":
            given_year=sys.argv[i+1]
            weather_file_parser = Parser()
            weather_file_parser.list_files(given_path,
                                           sys.argv[i], given_year)
            weather_file_parser.populate_weather_readings(given_path)
            results_generator = ResultsGenerator()
            results_generator.generate_results(
                weather_file_parser.weather_readings,
                sys.argv[i])
            report_generator = ReportGenerator(
                sys.argv[i],
                results_generator.generated_results)
            report_generator.print_report()
        elif sys.argv[i] == "-c":
            given_date = sys.argv[i+1].split("/")
            given_year = given_date[0]
            given_month = int(given_date[1])
            weather_file_parser = Parser()
            weather_file_parser.list_files(given_path, sys.argv[i],
                                           given_year, given_month)
            weather_file_parser.populate_weather_readings(given_path)
            results_generator = ResultsGenerator()
            results_generator.generate_results(
                weather_file_parser.weather_readings,
                sys.argv[i])
            report_generator = ReportGenerator(
                sys.argv[i],
                results_generator.generated_results)
            report_generator.print_report()
        i += 1
    exit()


if __name__=="__main__":
    main()