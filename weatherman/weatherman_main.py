import argparse

from weatherman_helper_func import *


def arg_parser():
    parser = argparse.ArgumentParser(description="Weatherman Part 1")
    parser.add_argument("file_path", nargs=1)
    parser.add_argument("-e", nargs="*")
    parser.add_argument("-a", nargs="*")
    parser.add_argument("-c", nargs="*")
    return parser.parse_args()


if __name__ == "__main__":
    parsed_args = arg_parser()
    file_path = parsed_args.file_path[0]
    if parsed_args.a:
        for query_date in parsed_args.a:
            data = FileReader.read_file(file_path, query_date)
            result = CalculateResults.month_result(data)
            PrintReports.month_averages(result)
    if parsed_args.e:
        for query_date in parsed_args.e:
            data = FileReader.read_file(file_path, query_date)
            result = CalculateResults.year_result(data)
            PrintReports.year_stats(result)
    if parsed_args.c:
        for query_date in parsed_args.c:
            data = FileReader.read_file(file_path, query_date)
            PrintReports.weather_graph(data)
