import argparse
from weather_report import *

reports = {"a": AveragesReport, "c": ChartsReport, "e": ExtremesReport}


def parse_arguments():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-a')
    args_parser.add_argument('-c')
    args_parser.add_argument('-e')
    args_parser.add_argument(dest='path')
    args = vars(args_parser.parse_args())
    path = args['path']
    del args['path']
    return args, path


def process_reports(path, report_args):
    for k in report_args:
        file_parser = WeatherReadingsPopulator(reports[k], path)
        file_parser.list_files(report_args[k])
        file_parser.populate_weather_readings()
        results_gen = ResultsGenerator(reports[k])
        results_gen.generate_results(file_parser.weather_readings)
        report_gen = ReportGenerator(reports[k], results_gen.generated_results)
        report_gen.print_report()


if __name__ == "__main__":
    cl_args, files_path = parse_arguments()
    process_reports(files_path, cl_args)
