from weatherman_repo.utils.file_utils import ParseFiles


class WeatherReadingData(object):
    """
    Data structure for holding each weather reading
    """

    def __init__(self, *args, **kwargs):
        self.file_path = kwargs.get('file_path', '')
        self.year = kwargs.get('year', '')
        self.month = kwargs.get('month', '')

    @property
    def get_weather_data(self):
        file_parser = ParseFiles.parse_data(self.file_path, self.year, self.month)
        for weather_data_entry in file_parser:
            for row in weather_data_entry:
                yield row


class WeatherDataCalculationResults(object):
    """
    Data structure for holding the calculations results.
    """
    def __init__(self):
        pass
