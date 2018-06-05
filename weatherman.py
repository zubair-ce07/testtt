import argparse
from calculate_results import ResultsGenerator
from generate_reports import ReportGenerator
from populate_weather_readings import WeatherReadingsPopulator


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
    file_parser = WeatherReadingsPopulator(cl_args.files_path)
    results_generator = ResultsGenerator()
    for year in cl_args.e_collection:
        file_parser.list_files("-e", year)
        file_parser.populate_weather_readings()
        results_generator.generate_results("-e", file_parser.weather_readings)
        report_generator = ReportGenerator("-e",
                                           results_generator.generated_results)
        report_generator.print_report()
    for month_year in cl_args.a_collection:
        file_parser.list_files("-a",
                               month_year.split("/")[0],
                               int(month_year.split("/")[1]))
        file_parser.populate_weather_readings()
        results_generator.generate_results("-a", file_parser.weather_readings)
        report_generator = ReportGenerator("-a",
                                           results_generator.generated_results)
        report_generator.print_report()
    for month_year in cl_args.c_collection:
        file_parser = WeatherReadingsPopulator(cl_args.files_path)
        file_parser.list_files("-c",
                               month_year.split("/")[0],
                               int(month_year.split("/")[1]))
        file_parser.populate_weather_readings()
        results_generator.generate_results("-c", file_parser.weather_readings)
        report_generator = ReportGenerator("-c",
                                           results_generator.generated_results)
        report_generator.print_report()


if __name__ == "__main__":
    main()
