import argparse
from weather_report import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='files_path', type=str)
    parser.add_argument('-a', action='append', dest='a_collection',
                        default=[], type=str)
    parser.add_argument('-c', action='append', dest='c_collection',
                        default=[], type=str)
    parser.add_argument('-e', action='append', dest='e_collection',
                        default=[], type=str)
    cl_args = parser.parse_args()
    for year in cl_args.e_collection:
        file_parser = WeatherReadingsPopulator(ReportStrategyE,
                                               cl_args.files_path)
        file_parser.list_files(year)
        file_parser.populate_weather_readings()
        results_generator = ResultsGenerator(ReportStrategyE)
        results_generator.generate_results(file_parser.weather_readings)
        report_generator = ReportGenerator(ReportStrategyE,
                                           results_generator.generated_results)
        report_generator.print_report()
    for month_year in cl_args.a_collection:
        file_parser = WeatherReadingsPopulator(ReportStrategyA,
                                               cl_args.files_path)
        file_parser.list_files(month_year)
        file_parser.populate_weather_readings()
        results_generator = ResultsGenerator(ReportStrategyA)
        results_generator.generate_results(file_parser.weather_readings)
        report_generator = ReportGenerator(ReportStrategyA,
                                           results_generator.generated_results)
        report_generator.print_report()
    for month_year in cl_args.c_collection:
        file_parser = WeatherReadingsPopulator(ReportStrategyC,
                                               cl_args.files_path)
        file_parser.list_files(month_year)
        file_parser.populate_weather_readings()
        results_generator = ResultsGenerator(ReportStrategyC)
        results_generator.generate_results(file_parser.weather_readings)
        report_generator = ReportGenerator(ReportStrategyC,
                                           results_generator.generated_results)
        report_generator.print_report()


if __name__ == "__main__":
    main()
