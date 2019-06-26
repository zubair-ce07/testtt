from weatherdata import YearlyWeatherParser, MonthlyWeatherParser
from reportgenrator import HighLowReportGenerator, AvgTemperatureReportGenerator


def main():
    # yearly_parser = YearlyWeatherParser(path='weatherfiles/', year=2004)
    # weather_data = yearly_parser.parse()
    # HighLowReportGenerator(weather_data).generate()

    monthly_parser = MonthlyWeatherParser(path='weatherfiles', year=2005, month=6)
    weather_data = monthly_parser.parse()
    AvgTemperatureReportGenerator(weather_data).generate()


if __name__ == '__main__':
    main()
