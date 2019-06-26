from weatherdata import YearlyWeatherParser
from reportgenrator import HighLowReportGenerator


def main():
    yearly_parser = YearlyWeatherParser(path='weatherfiles/', year=2004)
    weather_data = yearly_parser.parse()
    HighLowReportGenerator(weather_data).generate()


if __name__ == '__main__':
    main()
