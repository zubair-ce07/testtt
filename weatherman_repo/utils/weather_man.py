from .datastructures import WeatherReadingData
from .decorators import validate_input
from .design_patterns import Singleton


class WeatherMan(metaclass=Singleton):
    """
    Contains complete flow required for working of weather man.
    """
    def __init__(self):
        self.data = None

    @validate_input
    def year_result(self, *args, **kwargs):
        self.data = WeatherReadingData(
            data_path=kwargs.get('data_path'),
            year=kwargs.get('year_month')
        )
        for weather_data in self.data.get_weather_data:
            print(weather_data)

    @validate_input
    def year_with_month_result(self, *args, **kwarg):
        print('get year result')
        return 1

    @validate_input
    def month_bar_chart_result(self, *args, **kwarg):
        print('get year result')
        return 1

    def show_result(self, file_path, option, year_month):
        return getattr(self, '{}_result'.format(option))(file_path=file_path, year_month=year_month)
