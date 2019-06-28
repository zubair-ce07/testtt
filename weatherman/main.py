import argparse

from weatherparser import YearlyWeatherParser, MonthlyWeatherParser
from reportgenerator import HighLowReportGenerator, \
                            AverageTemperatureReportGenerator, \
                            HighLowTemperatureGraphReportGenerator, \
                            HighLowTemperatureSingleGraphReportGenerator


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='relative path to the dataset')
    parser.add_argument('-e', nargs=1, required=False, action='append')
    parser.add_argument('-a', nargs=1, required=False, action='append')
    parser.add_argument('-c', nargs=1, required=False, action='append')
    parser.add_argument('-b', nargs=1, required=False, action='append')
    args = parser.parse_args()
    dataset_path = args.path

    if args.e is not None:
        for arg in args.e:

            yearly_parser = YearlyWeatherParser(path=dataset_path,
                                                year=int(arg[0]))
            weather_data = yearly_parser.parse()

            report_generator = HighLowReportGenerator()
            report_generator.generate(weather_data)

    if args.a is not None:
        for arg in args.a:
            year, month = arg[0].split('/')
            monthly_parser = MonthlyWeatherParser(path=dataset_path,
                                                  month=int(month),
                                                  year=int(year))
            weather_data = monthly_parser.parse()
            report_generator = AverageTemperatureReportGenerator()
            report_generator.generate(weather_data)

    if args.c is not None:
        for arg in args.c:
            year, month = arg[0].split('/')
            monthly_parser = MonthlyWeatherParser(path=dataset_path,
                                                  month=int(month),
                                                  year=int(year))
            weather_data = monthly_parser.parse()
            report_generator = HighLowTemperatureGraphReportGenerator()
            report_generator.generate(weather_data)

    if args.b is not None:
        for arg in args.b:
            year, month = arg[0].split('/')
            monthly_parser = MonthlyWeatherParser(path=dataset_path,
                                                  month=int(month),
                                                  year=int(year))
            weather_data = monthly_parser.parse()
            report_generator = HighLowTemperatureSingleGraphReportGenerator()
            report_generator.generate(weather_data)


if __name__ == '__main__':
    main()
